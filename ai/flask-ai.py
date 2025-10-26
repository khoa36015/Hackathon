#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ai_onefile.py
- Train 1 mô hình sinh văn bản (generative) kiểu RNN/LSTM ở mức ký tự từ CSV
- Serve API bằng Flask (1 file duy nhất)
- Dùng: 
  pip install torch pandas flask
  python ai_onefile.py train --csv data.csv --text-col content --epochs 3
  python ai_onefile.py serve --host 0.0.0.0 --port 8000
"""

import os
import json
import math
import argparse
import random
from typing import Dict, List, Tuple

import pandas as pd
import torch
import torch.nn as nn
from flask import Flask, request, jsonify

# ---------------------------
# Utils: device & seed
# ---------------------------
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

def set_seed(seed: int = 42):
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

# ---------------------------
# Tokenization: character-level (hỗ trợ UTF-8 tốt cho tiếng Việt)
# ---------------------------
class CharVocab:
    def __init__(self, text: str, min_freq: int = 1):
        # Lấy tập ký tự xuất hiện
        freqs: Dict[str, int] = {}
        for ch in text:
            freqs[ch] = freqs.get(ch, 0) + 1
        # Ký tự đặc biệt
        self.pad = "<PAD>"
        self.unk = "<UNK>"
        self.specials = [self.pad, self.unk]
        # Lọc theo min_freq để né ký tự rác cực hiếm
        chars = [c for c, f in sorted(freqs.items(), key=lambda x: (-x[1], x[0])) if f >= min_freq]
        self.itos = self.specials + chars
        self.stoi = {s: i for i, s in enumerate(self.itos)}
        self.pad_id = self.stoi[self.pad]
        self.unk_id = self.stoi[self.unk]

    def encode(self, s: str) -> List[int]:
        return [self.stoi.get(ch, self.unk_id) for ch in s]

    def decode(self, ids: List[int]) -> str:
        return "".join(self.itos[i] for i in ids if i < len(self.itos))

    def __len__(self):
        return len(self.itos)

# ---------------------------
# Dataset tạo (input, target) theo sliding window
# ---------------------------
class CharDataset(torch.utils.data.Dataset):
    def __init__(self, ids: List[int], seq_len: int = 160):
        self.ids = ids
        self.seq_len = seq_len

    def __len__(self):
        # -1 để vẫn còn 1 token target
        return max(0, len(self.ids) - self.seq_len - 1)

    def __getitem__(self, idx):
        x = torch.tensor(self.ids[idx : idx + self.seq_len], dtype=torch.long)
        y = torch.tensor(self.ids[idx + 1 : idx + 1 + self.seq_len], dtype=torch.long)
        return x, y

# ---------------------------
# Model: Embedding -> LSTM -> Linear
# ---------------------------
class CharLSTM(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int = 256, hidden_dim: int = 512, num_layers: int = 2, dropout: float = 0.1):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, num_layers=num_layers, dropout=dropout, batch_first=True)
        self.proj = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x, hidden=None):
        # x: (B, T)
        e = self.embed(x)  # (B, T, E)
        out, hidden = self.lstm(e, hidden)  # (B, T, H)
        logits = self.proj(out)  # (B, T, V)
        return logits, hidden

# ---------------------------
# Training loop
# ---------------------------
def train_model(
    text: str,
    out_path: str = "ckpt.pt",
    seq_len: int = 160,
    batch_size: int = 64,
    epochs: int = 3,
    lr: float = 3e-3,
    min_freq: int = 1,
    grad_clip: float = 1.0,
):
    device = get_device()
    print(f"[Device] {device}")

    # Build vocab & ids
    vocab = CharVocab(text, min_freq=min_freq)
    ids = vocab.encode(text)

    # Split train/val
    n = len(ids)
    split = int(0.95 * n)
    train_ids, val_ids = ids[:split], ids[split:]

    train_ds = CharDataset(train_ids, seq_len=seq_len)
    val_ds = CharDataset(val_ids, seq_len=seq_len)
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    val_loader = torch.utils.data.DataLoader(val_ds, batch_size=batch_size, shuffle=False, drop_last=True)

    model = CharLSTM(len(vocab)).to(device)
    criterion = nn.CrossEntropyLoss()
    opt = torch.optim.AdamW(model.parameters(), lr=lr)

    best_val = float("inf")
    for epoch in range(1, epochs + 1):
        model.train()
        total = 0.0
        steps = 0
        for x, y in train_loader:
            x = x.to(device)
            y = y.to(device)
            logits, _ = model(x)  # (B, T, V)
            loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))
            opt.zero_grad()
            loss.backward()
            if grad_clip is not None:
                nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
            opt.step()
            total += loss.item()
            steps += 1
        train_loss = total / max(1, steps)

        val_loss = evaluate(model, val_loader, criterion, device)
        print(f"[Epoch {epoch}/{epochs}] train_loss={train_loss:.4f} val_loss={val_loss:.4f}")

        if val_loss < best_val:
            best_val = val_loss
            save_checkpoint(out_path, model, vocab, {
                "seq_len": seq_len,
                "embed_dim": model.embed.embedding_dim,
                "hidden_dim": model.proj.in_features,
                "num_layers": model.lstm.num_layers
            })
            print(f"  -> Saved best ckpt to {out_path}")

    print("[Done] Training complete.")

def evaluate(model, loader, criterion, device):
    model.eval()
    total = 0.0
    steps = 0
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device)
            logits, _ = model(x)
            loss = criterion(logits.view(-1, logits.size(-1)), y.view(-1))
            total += loss.item()
            steps += 1
    return total / max(1, steps)

def save_checkpoint(path: str, model: nn.Module, vocab: CharVocab, config: Dict):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    payload = {
        "state_dict": model.state_dict(),
        "vocab": {
            "itos": vocab.itos,
            "pad": vocab.pad,
            "unk": vocab.unk
        },
        "config": config
    }
    torch.save(payload, path)

def load_checkpoint(path: str, map_location=None):
    payload = torch.load(path, map_location=map_location or get_device())
    vocab_data = payload["vocab"]
    vocab = CharVocab(" ")  # dummy init
    vocab.itos = vocab_data["itos"]
    vocab.stoi = {s: i for i, s in enumerate(vocab.itos)}
    vocab.pad = vocab_data["pad"]
    vocab.unk = vocab_data["unk"]
    vocab.pad_id = vocab.stoi[vocab.pad]
    vocab.unk_id = vocab.stoi[vocab.unk]
    cfg = payload["config"]
    model = CharLSTM(vocab_size=len(vocab),
                     embed_dim=cfg.get("embed_dim", 256),
                     hidden_dim=cfg.get("hidden_dim", 512),
                     num_layers=cfg.get("num_layers", 2)).to(get_device())
    model.load_state_dict(payload["state_dict"])
    model.eval()
    return model, vocab, cfg

# ---------------------------
# Sampling / Generation
# ---------------------------
@torch.no_grad()
def sample(model: nn.Module, vocab: CharVocab, prompt: str = "", max_new_tokens: int = 100, temperature: float = 1.0, top_k: int = 0) -> str:
    device = get_device()
    model.eval()
    # Encode prompt
    context = torch.tensor([vocab.encode(prompt)], dtype=torch.long, device=device)
    hidden = None
    # Warm up with prompt
    if context.numel() > 0:
        _, hidden = model(context, hidden)

    last_token = context[:, -1] if context.numel() > 0 else torch.tensor([[vocab.stoi.get(" ", vocab.unk_id)]], device=device)

    out_ids: List[int] = []
    for _ in range(max_new_tokens):
        logits, hidden = model(last_token, hidden)  # shape (B=1, T=1, V)
        logits = logits[:, -1, :]  # (1, V)
        if temperature > 0:
            logits = logits / max(1e-6, temperature)
        probs = torch.softmax(logits, dim=-1)
        if top_k and top_k > 0:
            # top-k sampling
            values, indices = torch.topk(probs, k=min(top_k, probs.size(-1)))
            indices = indices[0]
            values = values[0] / values.sum()
            idx = indices[torch.multinomial(values, num_samples=1)]
        else:
            idx = torch.multinomial(probs, num_samples=1)
        token_id = idx.item()
        out_ids.append(token_id)
        last_token = idx.view(1, 1)
    return prompt + vocab.decode(out_ids)

# ---------------------------
# Data loading from CSV
# ---------------------------
def load_text_from_csv(csv_path: str, text_col: str) -> str:
    df = pd.read_csv(csv_path)
    if text_col not in df.columns:
        raise ValueError(f"Column '{text_col}' not found. Available: {list(df.columns)}")
    # Ghép tất cả văn bản lại; loại NaN
    texts = df[text_col].dropna().astype(str).tolist()
    # Thêm dấu xuống dòng để giúp model học ranh giới
    joined = "\n".join(texts)
    # Có thể lọc bớt ký tự control
    return joined

# ---------------------------
# Flask app
# ---------------------------
def create_app(model_path: str = "ckpt.pt"):
    app = Flask(__name__)
    device = get_device()
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Checkpoint '{model_path}' not found. Hãy train trước (python ai_onefile.py train ...) !")
    model, vocab, _ = load_checkpoint(model_path, map_location=device)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "device": str(device)})

    @app.get("/info")
    def info():
        return jsonify({
            "model": "CharLSTM-mini",
            "vocab_size": len(vocab),
            "note": "This is a tiny character-level generative model (toy, not DeepSeek)."
        })

    @app.post("/generate")
    def generate():
        data = request.get_json(force=True, silent=True) or {}
        prompt = data.get("prompt", "")
        max_new = int(data.get("max_new_tokens", 120))
        temperature = float(data.get("temperature", 0.9))
        top_k = int(data.get("top_k", 0))
        text = sample(model, vocab, prompt=prompt, max_new_tokens=max_new, temperature=temperature, top_k=top_k)
        return jsonify({"prompt": prompt, "completion": text})

    return app

# ---------------------------
# CLI
# ---------------------------
def main():
    parser = argparse.ArgumentParser(description="Tiny one-file Generative AI (Char-LSTM) with Flask API.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # Train
    p_train = sub.add_parser("train", help="Train from CSV")
    p_train.add_argument("--csv", required=True, help="CSV path")
    p_train.add_argument("--text-col", required=True, help="Column name containing text")
    p_train.add_argument("--out", default="ckpt.pt", help="Output checkpoint path")
    p_train.add_argument("--seq-len", type=int, default=160)
    p_train.add_argument("--batch-size", type=int, default=64)
    p_train.add_argument("--epochs", type=int, default=3)
    p_train.add_argument("--lr", type=float, default=3e-3)
    p_train.add_argument("--min-freq", type=int, default=1)
    p_train.add_argument("--seed", type=int, default=42)

    # Serve
    p_serve = sub.add_parser("serve", help="Run Flask API")
    p_serve.add_argument("--model", default="ckpt.pt", help="Checkpoint path")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args()
    set_seed(args.seed if hasattr(args, "seed") else 42)

    if args.cmd == "train":
        text = load_text_from_csv(args.csv, args.text_col)
        # Gợi ý nhỏ nếu dữ liệu quá ít
        if len(text) < 1000:
            print("[Warning] Dữ liệu huấn luyện khá ít; cân nhắc gom thêm văn bản để chất lượng tốt hơn.")
        train_model(
            text=text,
            out_path=args.out,
            seq_len=args.seq_len,
            batch_size=args.batch_size,
            epochs=args.epochs,
            lr=args.lr,
            min_freq=args.min_freq,
        )
    elif args.cmd == "serve":
        app = create_app(args.model)
        app.run(host=args.host, port=args.port, debug=False)
    else:
        raise ValueError("Unknown command")

if __name__ == "__main__":
    main()
