<script>
  import { onMount } from 'svelte';
  import { session } from '$lib/stores/session';
  import { sendAgentMessage } from '$lib/api';
  import Header from '$lib/components/Header.svelte';

  let messages = [];
  let inputMessage = '';
  let chatContainer;
  let isLoading = false;

  function sendMessage() {
    if (inputMessage.trim() && !isLoading) {
      const userMessage = inputMessage.trim();
      messages = [...messages, { text: userMessage, sender: 'user' }];
      inputMessage = '';
      isLoading = true;

      // Call the API
      sendAgentMessage(userMessage)
        .then(response => {
          if (response.answer) {
            let aiMessage = response.answer;
            if (response.tips && response.tips.length > 0) {
              aiMessage += '\n\n💡 Mẹo: ' + response.tips.join('\n• ');
            }
            messages = [...messages, { text: aiMessage, sender: 'ai' }];
          } else {
            messages = [...messages, { text: 'Xin lỗi, có lỗi xảy ra. Vui lòng thử lại.', sender: 'ai' }];
          }
        })
        .catch(error => {
          console.error('Error sending message:', error);
          messages = [...messages, { text: 'Xin lỗi, không thể kết nối đến server. Vui lòng thử lại.', sender: 'ai' }];
        })
        .finally(() => {
          isLoading = false;
        });
    }
  }

  function handleKeydown(event) {
    if (event.key === 'Enter' && !isLoading) {
      sendMessage();
    }
  }

  onMount(() => {
    if (chatContainer) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  });
</script>

<svelte:head>
  <title>AI Chatbot - Miền Tây Travel</title>
</svelte:head>

<Header />

<section class="px-6 py-10 bg-linear-to-b from-sky-50 to-white">
  <h2 class="text-3xl font-bold text-center text-sky-800 mb-8">Trợ lý AI Miền Tây</h2>

  <!-- Chat Container -->
  <div class="max-w-4xl mx-auto">
    <div
      bind:this={chatContainer}
      class="bg-white rounded-2xl shadow-lg p-6 overflow-y-auto max-h-96 mb-6"
    >
      {#each messages as message}
        <div class="mb-4 {message.sender === 'user' ? 'text-right' : 'text-left'}">
          <div class="inline-block px-4 py-2 rounded-lg {message.sender === 'user' ? 'bg-sky-600 text-white' : 'bg-gray-200 text-gray-800'} max-w-xs lg:max-w-md">
            {message.text}
          </div>
        </div>
      {/each}
      {#if messages.length === 0}
        <div class="text-center text-gray-500 py-8">
          <p class="text-lg">Chào mừng bạn đến với Trợ lý AI!</p>
          <p>Hỏi anh Ba Sỉn về du lịch Miền Tây đi.</p>
        </div>
      {/if}
      {#if isLoading}
        <div class="text-left mb-4">
          <div class="inline-block px-4 py-2 rounded-lg bg-gray-200 text-gray-800">
            <div class="flex items-center gap-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
              Anh Ba Sỉn đang trả lời...
            </div>
          </div>
        </div>
      {/if}
    </div>

    <!-- Input Area -->
    <div class="flex gap-2">
      <input
        type="text"
        bind:value={inputMessage}
        placeholder="Hỏi về du lịch Miền Tây..."
        class="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-sky-500 shadow-md"
        on:keydown={handleKeydown}
        disabled={isLoading}
      />
      <button
        on:click={sendMessage}
        class="bg-sky-600 hover:bg-sky-700 text-white px-6 py-3 rounded-full shadow-md transition duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={isLoading || !inputMessage.trim()}
      >
        Gửi
      </button>
    </div>
  </div>
</section>
