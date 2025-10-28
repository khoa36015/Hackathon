from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

#du lieu
dulieu = {
    "an_giang": {
        "ten": "An Giang",
        "mo_ta": "Vùng đất tâm linh và hùng vĩ, nơi có núi Sam, Bà Chúa Xứ và cảnh quan sông núi đặc trưng.",
        "anh_dai_dien": "https://cdn.tuoitre.vn/2022/8/8/ba-chua-xu-nui-sam-16599559621721904690651.jpg",
        "dia_diem": {
            "Núi Sam": {
                "mo_ta": "Điểm du lịch tâm linh nổi tiếng với Miếu Bà Chúa Xứ linh thiêng.",
                "anh": "https://media-cdn-v2.laodong.vn/storage/newsportal/2023/5/15/1187408/Nui-Sam-2.jpg"
            },
            "Rừng Tràm Trà Sư": {
                "mo_ta": "Khu sinh thái ngập nước tiêu biểu của miền Tây, nổi tiếng với vẻ đẹp xanh mướt.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2017/08/rung-tram-tra-su.jpg"
            },
            "Chợ nổi Long Xuyên": {
                "mo_ta": "Nơi buôn bán nhộn nhịp trên sông Hậu, mang đậm văn hóa sông nước.",
                "anh": "https://mia.vn/media/uploads/blog-du-lich/cho-noi-long-xuyen-01-1658232468.jpg"
            },
            "Hồ Tà Pạ": {
                "mo_ta": "‘Tuyệt tình cốc’ của miền Tây với làn nước xanh ngọc bích.",
                "anh": "https://ik.imagekit.io/tvlk/blog/2023/08/ho-ta-pa-an-giang-5-1024x683.jpg"
            }
        },
        "van_hoa": [
            "Lễ hội Vía Bà Chúa Xứ Núi Sam",
            "Giao thoa văn hóa Việt - Khmer - Hoa độc đáo"
        ],
        "mon_an": {
            "Bún cá Châu Đốc": {
                "mo_ta": "Món đặc sản trứ danh với hương vị đậm đà.",
                "anh": "https://cdn.tgdd.vn/Files/2020/12/15/1313292/cach-nau-bun-ca-chau-doc-an-giang-dam-da-vi-mien-tay-202112311025384474.jpg"
            },
            "Mắm Châu Đốc": {
                "mo_ta": "Đặc sản làm từ cá lên men, hương vị đặc trưng miền Tây.",
                "anh": "https://cdn.tgdd.vn/Files/2020/09/02/1287168/huong-dan-cach-lam-mam-ca-linh-chau-doc-thom-ngon-dung-dieu-202109021135522788.jpg"
            },
            "Bánh xèo Núi Sam": {
                "mo_ta": "Vỏ giòn, nhân tôm thịt, ăn kèm rau rừng.",
                "anh": "https://cdn.tgdd.vn/Files/2021/08/24/1378461/cach-lam-banh-xeo-mien-tay-gion-lau-don-gian-ngon-nhu-ngoai-hang-202108240957539697.jpg"
            }
        }
    },

    "kien_giang": {
        "ten": "Kiên Giang",
        "mo_ta": "Thiên đường biển đảo của miền Tây, nổi bật với Phú Quốc, Nam Du và Hòn Sơn.",
        "anh_dai_dien": "https://vcdn1-dulich.vnecdn.net/2022/04/19/phuquoc-1650358674-9330-1650358805.jpg",
        "dia_diem": {
            "Phú Quốc": {
                "mo_ta": "Hòn đảo ngọc với biển xanh và cát trắng mịn.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2017/05/dao-phu-quoc.jpg"
            },
            "Nam Du": {
                "mo_ta": "Quần đảo hoang sơ với nước biển trong vắt.",
                "anh": "https://cdn.tgdd.vn/Files/2021/01/27/1325763/kinh-nghiem-du-lich-dao-nam-du-202101270857394514.jpg"
            },
            "Hòn Sơn": {
                "mo_ta": "Thiên nhiên trong lành, là điểm đến yêu thích của dân phượt.",
                "anh": "https://cdn.tgdd.vn/Files/2021/01/25/1325500/kinh-nghiem-du-lich-hon-son-202101251346434768.jpg"
            },
            "Rạch Giá": {
                "mo_ta": "Thành phố biển hiện đại, trung tâm hành chính của Kiên Giang.",
                "anh": "https://vcdn1-dulich.vnecdn.net/2020/05/29/rachgia-1590757163.jpg"
            }
        },
        "van_hoa": [
            "Lễ hội Nguyễn Trung Trực tại Rạch Giá.",
            "Văn hóa biển đảo độc đáo, đời sống gắn liền với ngư nghiệp."
        ],
        "mon_an": {
            "Gỏi cá trích": {
                "mo_ta": "Món đặc sản Phú Quốc nổi tiếng, ăn kèm rau rừng.",
                "anh": "https://cdn.tgdd.vn/Files/2021/03/15/1335265/cach-lam-goi-ca-trich-phu-quoc-202103151117369707.jpg"
            },
            "Bún quậy Kiên Giang": {
                "mo_ta": "Sợi bún tươi trộn nước chấm tự pha, hương vị độc đáo.",
                "anh": "https://cdn.tgdd.vn/Files/2021/07/22/1371763/cach-nau-bun-quay-kien-giang-dam-da-chuan-vi-mien-tay-202107220951429826.jpg"
            },
            "Còi biên mai nướng": {
                "mo_ta": "Đặc sản biển Phú Quốc được nhiều du khách ưa chuộng.",
                "anh": "https://cdn.tgdd.vn/Files/2020/09/16/1289940/cach-lam-coi-bien-mai-nuong-muoi-ot-thom-ngon-kho-cuong-202009161401264523.jpg"
            }
        }
    },

    "ben_tre": {
        "ten": "Bến Tre",
        "mo_ta": "Xứ dừa yên bình, quê hương của những làng nghề thủ công và món ngon miệt vườn.",
        "anh_dai_dien": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2018/07/du-lich-ben-tre.jpg",
        "dia_diem": {
            "Cồn Phụng": {
                "mo_ta": "Điểm du lịch sinh thái nổi tiếng ven sông Tiền.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2018/07/con-phung-ben-tre.jpg"
            },
            "Làng nghề kẹo dừa": {
                "mo_ta": "Nổi tiếng khắp cả nước, du khách có thể tham quan quy trình làm kẹo.",
                "anh": "https://cdn.tgdd.vn/Files/2020/10/30/1300968/cach-lam-keo-dua-ben-tre-thom-ngon-beo-ngay-don-gian-tai-nha-202010301614259606.jpg"
            },
            "Vườn trái cây Chợ Lách": {
                "mo_ta": "Thiên đường cây ăn trái quanh năm trĩu quả.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2018/07/du-lich-cho-lach-ben-tre.jpg"
            },
            "Nhà cổ Huỳnh Phủ": {
                "mo_ta": "Công trình kiến trúc cổ mang dấu ấn văn hóa miền Tây.",
                "anh": "https://cdn.tgdd.vn/Files/2020/11/04/1301655/nha-co-huynh-phu-ben-tre-diem-den-van-hoa-doc-dao-202011040920223997.jpg"
            }
        },
        "van_hoa": [
            "Lễ hội Nghinh Ông Bến Tre",
            "Văn hóa miệt vườn và nghề thủ công từ dừa"
        ],
        "mon_an": {
            "Kẹo dừa": {
                "mo_ta": "Đặc sản nổi tiếng của Bến Tre, ngọt béo và thơm lừng.",
                "anh": "https://cdn.tgdd.vn/Files/2020/10/30/1300968/cach-lam-keo-dua-ben-tre-thom-ngon-beo-ngay-don-gian-tai-nha-202010301614259606.jpg"
            },
            "Cá kho tộ": {
                "mo_ta": "Món ăn dân dã, đậm vị quê hương miền Tây.",
                "anh": "https://cdn.tgdd.vn/Files/2020/05/04/1250075/cach-lam-ca-kho-to-don-gian-dam-da-thom-ngon-dung-vi-202005041557589078.jpg"
            },
            "Chuối đập nướng": {
                "mo_ta": "Món ăn vặt giản dị nhưng đậm đà hương vị miệt vườn.",
                "anh": "https://cdn.tgdd.vn/Files/2021/06/11/1361681/cach-lam-chuoi-nuong-nuoc-cot-dua-thom-ngon-chuan-vi-202106111004592986.jpg"
            }
        }
    },

    "can_tho": {
        "ten": "Cần Thơ",
        "mo_ta": "Trung tâm kinh tế, văn hóa của miền Tây, nổi tiếng với chợ nổi Cái Răng và bến Ninh Kiều.",
        "anh_dai_dien": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2017/05/ben-ninh-kieu-can-tho.jpg",
        "dia_diem": {
            "Bến Ninh Kiều": {
                "mo_ta": "Biểu tượng của thành phố, nơi du khách ngắm sông Hậu và thành phố về đêm.",
                "anh": "https://statics.vinpearl.com/ben-ninh-kieu-1_1662709080.jpg"
            },
            "Chợ nổi Cái Răng": {
                "mo_ta": "Nơi thể hiện rõ nhất nét văn hóa sông nước miền Tây.",
                "anh": "https://cdn.tgdd.vn/Files/2021/02/18/1329789/kinh-nghiem-du-lich-cho-noi-cai-rang-can-tho-202102181618593506.jpg"
            },
            "Nhà cổ Bình Thủy": {
                "mo_ta": "Ngôi nhà cổ hơn 100 năm tuổi, pha trộn kiến trúc Đông - Tây.",
                "anh": "https://vcdn1-dulich.vnecdn.net/2021/01/19/nha-co-binh-thuy-1-1611050345.jpg"
            },
            "Cầu Cần Thơ": {
                "mo_ta": "Cây cầu dây văng lớn nhất miền Tây, biểu tượng hiện đại của vùng.",
                "anh": "https://cdn.tgdd.vn/Files/2020/09/16/1289909/cau-can-tho-202009161215357642.jpg"
            }
        },
        "van_hoa": [
            "Văn hóa chợ nổi đặc trưng",
            "Con người hiền hòa, hiếu khách"
        ],
        "mon_an": {
            "Lẩu mắm Cần Thơ": {
                "mo_ta": "Món ăn trứ danh miền sông nước với mùi vị đậm đà.",
                "anh": "https://cdn.tgdd.vn/Files/2020/05/22/1253749/cach-nau-lau-mam-can-tho-thom-ngon-chuan-vi-202005221152013308.jpg"
            },
            "Ốc nướng tiêu": {
                "mo_ta": "Món ăn dân dã, cay thơm, thường thấy ở các quán ven sông.",
                "anh": "https://cdn.tgdd.vn/Files/2020/06/02/1257089/cach-lam-oc-buou-nuong-tieu-xanh-202006021037247080.jpg"
            },
            "Bánh cống Cần Thơ": {
                "mo_ta": "Vỏ giòn rụm, nhân tôm thịt, chấm nước mắm chua ngọt.",
                "anh": "https://cdn.tgdd.vn/Files/2020/07/15/1267459/cach-lam-banh-cong-can-tho-thom-ngon-gion-rum-202007150900176211.jpg"
            }
        }
    },

    "ca_mau": {
        "ten": "Cà Mau",
        "mo_ta": "Mảnh đất cực Nam của Tổ quốc, nơi có Mũi Cà Mau thiêng liêng và hệ sinh thái rừng ngập mặn độc đáo.",
        "anh_dai_dien": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2017/05/mui-ca-mau.jpg",
        "dia_diem": {
            "Mũi Cà Mau": {
                "mo_ta": "Cột mốc thiêng liêng nơi tận cùng đất nước.",
                "anh": "https://cdn.tgdd.vn/Files/2021/07/14/1370947/mui-ca-mau-diem-den-thieng-lieng-cua-to-quoc-202107141057273915.jpg"
            },
            "Rừng U Minh Hạ": {
                "mo_ta": "Khu dự trữ sinh quyển, nơi sinh sống của nhiều loài động vật quý hiếm.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2017/05/uminhha.jpg"
            },
            "Hòn Đá Bạc": {
                "mo_ta": "Quần thể đá granite kỳ vĩ nằm ven biển.",
                "anh": "https://cdn.tgdd.vn/Files/2020/09/14/1289554/hon-da-bac-ca-mau-202009141152518548.jpg"
            },
            "Chợ nổi Cà Mau": {
                "mo_ta": "Nơi giao thương nhộn nhịp giữa các ghe hàng trên sông.",
                "anh": "https://cdn.tgdd.vn/Files/2021/06/29/1363743/cho-noi-ca-mau-diem-den-doc-dao-mang-net-van-hoa-song-nuoc-202106290946027267.jpg"
            }
        },
        "van_hoa": [
            "Lễ hội Nghinh Ông Sông Đốc",
            "Văn hóa người Khmer và Hoa hòa quyện"
        ],
        "mon_an": {
            "Ba khía muối": {
                "mo_ta": "Đặc sản trứ danh, mặn mà hương vị biển Tây Nam.",
                "anh": "https://cdn.tgdd.vn/Files/2021/02/03/1328589/cach-lam-ba-khia-muoi-ca-mau-chuan-vi-mien-tay-202102031411265999.jpg"
            },
            "Lẩu mắm U Minh": {
                "mo_ta": "Món ăn dân dã, quy tụ tinh hoa ẩm thực Cà Mau.",
                "anh": "https://cdn.tgdd.vn/Files/2021/05/05/1354479/cach-nau-lau-mam-ca-mau-dam-da-huong-vi-mien-tay-202105051024514301.jpg"
            },
            "Cua Cà Mau": {
                "mo_ta": "Nổi tiếng cả nước với thịt ngọt, chắc và thơm.",
                "anh": "https://cdn.tgdd.vn/Files/2021/05/05/1354479/cua-ca-mau-202105051024514301.jpg"
            }
        }
    },

    "dong_thap": {
        "ten": "Đồng Tháp",
        "mo_ta": "Miền sen hồng rực rỡ, với những cánh đồng sen và làng hoa Sa Đéc.",
        "anh_dai_dien": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2017/05/lang-hoa-sa-dec.jpg",
        "dia_diem": {
            "Làng hoa Sa Đéc": {
                "mo_ta": "Thiên đường hoa rực rỡ quanh năm.",
                "anh": "https://cdn.tgdd.vn/Files/2021/01/26/1325649/lang-hoa-sa-dec-202101261548595518.jpg"
            },
            "Khu du lịch Xẻo Quýt": {
                "mo_ta": "Khu rừng tràm lịch sử, gắn liền kháng chiến.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2018/04/xeo-quyt.jpg"
            },
            "Tràm Chim Tam Nông": {
                "mo_ta": "Nơi trú ngụ của hàng trăm loài chim quý hiếm.",
                "anh": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2018/04/tram-chim-tam-nong.jpg"
            },
            "Nhà cổ Huỳnh Thủy Lê": {
                "mo_ta": "Công trình kiến trúc Pháp cổ nổi tiếng.",
                "anh": "https://cdn.tgdd.vn/Files/2020/10/29/1300708/nha-co-huynh-thuy-le-dong-thap-202010291539526437.jpg"
            }
        },
        "van_hoa": [
            "Lễ hội Sen Đồng Tháp",
            "Tình người miền sông nước chân chất, hiền hòa"
        ],
        "mon_an": {
            "Hủ tiếu Sa Đéc": {
                "mo_ta": "Sợi hủ tiếu dẻo, nước dùng ngọt thanh đặc trưng.",
                "anh": "https://cdn.tgdd.vn/Files/2021/02/18/1329802/cach-nau-hu-tieu-sa-dec-dam-da-chuan-vi-202102181627325027.jpg"
            },
            "Chuột đồng nướng": {
                "mo_ta": "Đặc sản dân dã, giòn thơm hấp dẫn.",
                "anh": "https://cdn.tgdd.vn/Files/2021/06/14/1362042/cach-lam-chuot-dong-nuong-dam-da-huong-vi-mien-tay-202106141021386057.jpg"
            },
            "Xôi ngũ sắc": {
                "mo_ta": "Món xôi đặc trưng được làm từ gạo nếp thơm.",
                "anh": "https://cdn.tgdd.vn/Files/2021/05/13/1356017/cach-nau-xoi-ngu-sac-dep-mat-ngon-mieng-202105131540239567.jpg"
            }
        }
    },

    "soc_trang": {
        "ten": "Sóc Trăng",
        "mo_ta": "Vùng đất giao thoa văn hóa Việt - Hoa - Khmer, nổi bật với chùa Dơi và chùa Chén Kiểu.",
        "anh_dai_dien": "https://cdn.vntrip.vn/cam-nang/wp-content/uploads/2018/04/chua-doi-soc-trang.jpg",
        "dia_diem": {
            "Chùa Dơi": {
                "mo_ta": "Ngôi chùa Khmer cổ kính, nơi sinh sống của hàng ngàn con dơi.",
                "anh": "https://cdn.tgdd.vn/Files/2021/02/25/1330431/chua-doi-soc-trang-202102251513182083.jpg"
            },
            "Chùa Chén Kiểu": {
                "mo_ta": "Ngôi chùa độc đáo với tường khảm chén sứ.",
                "anh": "https://cdn.tgdd.vn/Files/2021/03/05/1332111/chua-chen-kieu-soc-trang-202103051107496950.jpg"
            },
            "Khu du lịch Hồ Nước Ngọt": {
                "mo_ta": "Điểm thư giãn lý tưởng giữa lòng thành phố.",
                "anh": "https://cdn.tgdd.vn/Files/2021/06/11/1361642/ho-nuoc-ngot-soc-trang-diem-den-du-lich-hap-dan-202106111014285207.jpg"
            },
            "Chợ nổi Ngã Năm": {
                "mo_ta": "Chợ nổi giao thương tấp nập trên sông.",
                "anh": "https://cdn.tgdd.vn/Files/2021/03/03/1331846/cho-noi-nga-nam-soc-trang-202103031529493914.jpg"
            }
        },
        "van_hoa": [
            "Lễ hội Oóc Om Bóc",
            "Văn hóa chùa chiền Khmer đậm sắc màu"
        ],
        "mon_an": {
            "Bún nước lèo Sóc Trăng": {
                "mo_ta": "Món ăn biểu tượng của vùng, kết hợp cá, tôm, heo quay.",
                "anh": "https://cdn.tgdd.vn/Files/2021/03/25/1336676/cach-nau-bun-nuoc-leo-soc-trang-202103251034349539.jpg"
            },
            "Bánh pía": {
                "mo_ta": "Đặc sản nổi tiếng toàn quốc, nhân sầu riêng trứng muối.",
                "anh": "https://cdn.tgdd.vn/Files/2020/07/07/1265593/cach-lam-banh-pia-soc-trang-thom-ngon-de-lam-202007071115414888.jpg"
            },
            "Bún gỏi dà": {
                "mo_ta": "Hương vị chua ngọt đặc trưng, hấp dẫn lạ miệng.",
                "anh": "https://cdn.tgdd.vn/Files/2020/06/18/1262036/cach-nau-bun-goi-da-chuan-vi-mien-tay-202006181357219743.jpg"
            }
        }
    },

    "haugiang": {
        "ten": "Hậu Giang",
        "mo_ta": "Trái tim của miền Tây, nơi lưu giữ nét đẹp văn hóa sông nước và những khu sinh thái miệt vườn đặc trưng.",
        "anh_dai_dien": "https://media.vov.vn/sites/default/files/styles/large/public/2021-03/lung-ngoc-hoang.jpg",
        "dia_diem": {
            "Khu du lịch sinh thái Lung Ngọc Hoàng": {
                "mo_ta": "Khu sinh thái đẹp với hệ sinh thái đa dạng.",
                "anh": "https://media.vov.vn/sites/default/files/styles/large/public/2021-03/lung-ngoc-hoang.jpg"
            },
            "Chợ nổi Ngã Bảy": {
                "mo_ta": "Điểm giao thương sầm uất trên sông.",
                "anh": "https://mia.vn/media/uploads/blog-du-lich/cho-noi-nga-bay-hau-giang-164.jpg"
            }
        },
        "van_hoa": [
            "Đậm đà bản sắc Nam Bộ, nổi bật với đờn ca tài tử và lễ hội Ok Om Bok của người Khmer",
            "Người dân chân chất, thân thiện và yêu lao động"
        ],
        "mon_an": {
            "Lẩu mắm Hậu Giang": {
                "mo_ta": "Món ăn đặc trưng của vùng sông nước.",
                "anh": "https://statics.vinpearl.com/lau-mam-mien-tay-3_1629455540.jpg"
            },
            "Bánh xèo củ hủ dừa": {
                "mo_ta": "Bánh xèo độc đáo với nhân củ hủ dừa.",
                "anh": "https://cdn.tgdd.vn/2020/10/CookProduct/thumb-banh-xeo-cu-hu-dua-thumbnail.jpg"
            }
        }
    },

    "travinh": {
        "ten": "Trà Vinh",
        "mo_ta": "Vùng đất giao thoa văn hóa Việt - Khmer với nhiều ngôi chùa cổ kính và di sản văn hóa phong phú.",
        "anh_dai_dien": "https://statics.vinpearl.com/ao-ba-om-tra-vinh-1_1667377751.jpg",
        "dia_diem": {
            "Ao Bà Om": {
                "mo_ta": "Di tích lịch sử văn hóa nổi tiếng của Trà Vinh.",
                "anh": "https://statics.vinpearl.com/ao-ba-om-tra-vinh-1_1667377751.jpg"
            },
            "Chùa Âng": {
                "mo_ta": "Ngôi chùa Khmer cổ kính với kiến trúc độc đáo.",
                "anh": "https://statics.vinpearl.com/chua-ang-tra-vinh-1_1667462291.jpg"
            }
        },
        "van_hoa": [
            "Nổi bật với lễ hội Ok Om Bok và kiến trúc chùa Khmer độc đáo",
            "Âm nhạc và ẩm thực mang đậm bản sắc Khmer Nam Bộ"
        ],
        "mon_an": {
            "Bún nước lèo Trà Vinh": {
                "mo_ta": "Món ăn truyền thống của người Khmer.",
                "anh": "https://cdn.tgdd.vn/2021/02/CookProduct/thumb-bun-nuoc-leo-tra-vinh-thumbnail.jpg"
            },
            "Bánh canh Bến Có": {
                "mo_ta": "Đặc sản nổi tiếng của Trà Vinh.",
                "anh": "https://cdn.tgdd.vn/2021/04/CookProduct/thumb-banh-canh-ben-co-thumbnail.jpg"
            }
        }
    },

    "baclieu": {
        "ten": "Bạc Liêu",
        "mo_ta": "Nổi tiếng với công tử Bạc Liêu, đờn ca tài tử và cánh đồng điện gió khổng lồ ven biển.",
        "anh_dai_dien": "https://statics.vinpearl.com/canh-dong-dien-gio-bac-lieu_1667445397.jpg",
        "dia_diem": {
            "Cánh đồng điện gió Bạc Liêu": {
                "mo_ta": "Công trình năng lượng sạch hiện đại bậc nhất Việt Nam.",
                "anh": "https://statics.vinpearl.com/canh-dong-dien-gio-bac-lieu_1667445397.jpg"
            },
            "Nhà công tử Bạc Liêu": {
                "mo_ta": "Di tích lịch sử gắn liền với giai thoại về công tử Bạc Liêu.",
                "anh": "https://statics.vinpearl.com/nha-cong-tu-bac-lieu_1667445409.jpg"
            }
        },
        "van_hoa": [
            "Cái nôi của đờn ca tài tử Nam Bộ – di sản phi vật thể UNESCO",
            "Con người Bạc Liêu hào sảng, hiếu khách và giàu lòng nhân ái"
        ],
        "mon_an": {
            "Bánh củ cải Bạc Liêu": {
                "mo_ta": "Món bánh truyền thống đặc trưng của Bạc Liêu.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookRecipe/GalleryStep/thanh-pham-28.jpg"
            },
            "Ba khía muối": {
                "mo_ta": "Đặc sản nổi tiếng vùng ven biển.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookRecipe/GalleryStep/ba-khia-muoi-1.jpg"
            }
        }
    },

    "vinhlong": {
        "ten": "Vĩnh Long",
        "mo_ta": "Nằm giữa hai nhánh sông Tiền và sông Hậu, Vĩnh Long là vùng đất miệt vườn trù phú và đậm đà bản sắc Nam Bộ.",
        "anh_dai_dien": "https://statics.vinpearl.com/cu-lao-an-binh-vinh-long.jpg",
        "dia_diem": {
            "Cù Lao An Bình": {
                "mo_ta": "Hòn đảo xanh mát giữa sông với vườn cây ăn trái sum suê.",
                "anh": "https://statics.vinpearl.com/cu-lao-an-binh-vinh-long.jpg"
            },
            "Chợ nổi Trà Ôn": {
                "mo_ta": "Điểm giao thương sầm uất trên sông nước.",
                "anh": "https://statics.vinpearl.com/cho-noi-tra-on-vinh-long.jpg"
            }
        },
        "van_hoa": [
            "Người dân hiền hòa, gắn bó với nghề làm vườn và đờn ca tài tử",
            "Nhiều làng nghề truyền thống và lễ hội miệt vườn đặc sắc"
        ],
        "mon_an": {
            "Cá tai tượng chiên xù": {
                "mo_ta": "Món ăn đặc sản từ cá tai tượng.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookProduct/ca-tai-tuong-chien-xu.jpg"
            },
            "Bánh xèo Vĩnh Long": {
                "mo_ta": "Bánh xèo đặc trưng vùng miệt vườn.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookProduct/banh-xeo-vinh-long.jpg"
            }
        }
    },

    "longan": {
        "ten": "Long An",
        "mo_ta": "Cửa ngõ miền Tây Nam Bộ, nổi tiếng với vùng trồng thanh long và di tích lịch sử phong phú.",
        "anh_dai_dien": "https://statics.vinpearl.com/lang-noi-tan-lap-long-an.jpg",
        "dia_diem": {
            "Làng nổi Tân Lập": {
                "mo_ta": "Khu du lịch sinh thái độc đáo với hệ sinh thái rừng tràm.",
                "anh": "https://statics.vinpearl.com/lang-noi-tan-lap-long-an.jpg"
            },
            "Nhà trăm cột": {
                "mo_ta": "Di tích kiến trúc độc đáo với 100 cột gỗ quý.",
                "anh": "https://statics.vinpearl.com/nha-tram-cot-long-an.jpg"
            }
        },
        "van_hoa": [
            "Là nơi giao thoa giữa miền Đông và miền Tây, vừa hiện đại vừa mang nét quê yên bình",
            "Có nhiều lễ hội truyền thống như lễ hội Vía Bà Ngũ Hành, lễ hội Làm Chay"
        ],
        "mon_an": {
            "Thanh long chấm muối ớt": {
                "mo_ta": "Đặc sản từ trái thanh long nổi tiếng.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookProduct/thanh-long-cham-muoi-ot.jpg"
            },
            "Bánh canh tôm": {
                "mo_ta": "Món ăn dân dã đặc trưng của vùng.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookProduct/banh-canh-tom-long-an.jpg"
            }
        }
    },

    "tiengiang": {
        "ten": "Tiền Giang",
        "mo_ta": "Cửa ngõ của miền Tây Nam Bộ, nổi tiếng với chợ nổi Cái Bè, cù lao Thới Sơn và đặc sản miệt vườn.",
        "anh_dai_dien": "https://statics.vinpearl.com/cu-lao-thoi-son-tien-giang.jpg",
        "dia_diem": {
            "Cù Lao Thới Sơn": {
                "mo_ta": "Hòn đảo xinh đẹp với vườn cây ăn trái sum suê.",
                "anh": "https://statics.vinpearl.com/cu-lao-thoi-son-tien-giang.jpg"
            },
            "Chợ nổi Cái Bè": {
                "mo_ta": "Khu chợ nổi sầm uất trên sông Tiền.",
                "anh": "https://statics.vinpearl.com/cho-noi-cai-be-tien-giang.jpg"
            }
        },
        "van_hoa": [
            "Gắn bó với nghề trồng cây ăn trái và du lịch sinh thái sông nước",
            "Có nhiều lễ hội dân gian đặc sắc như lễ hội Nghinh Ông và đờn ca tài tử"
        ],
        "mon_an": {
            "Hủ tiếu Mỹ Tho": {
                "mo_ta": "Món ăn nổi tiếng với nước dùng đặc trưng.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookProduct/hu-tieu-my-tho.jpg"
            },
            "Chuối ngự nướng": {
                "mo_ta": "Món ăn vặt đặc sản từ chuối ngự.",
                "anh": "https://cdn.tgdd.vn/2020/08/CookProduct/chuoi-ngut-nuong-tien-giang.jpg"
            }
        }
    }
}

# Danh sách mã tỉnh thuộc miền Tây (trùng với key trong dulieu)
MEKONG_KEYS = [
    "an_giang", "kien_giang", "ben_tre", "can_tho", "ca_mau",
    "dong_thap", "soc_trang", "haugiang", "travinh", "baclieu",
    "vinhlong", "longan", "tiengiang"
]

def pick_fields(province_id: str, data: dict) -> dict:
    """Chuẩn hóa record trả về cho frontend."""
    return {
        "id": province_id,  # id = mã tỉnh (key)
        "ten": data.get("ten"),
        "mo_ta": data.get("mo_ta"),
        "anh_dai_dien": data.get("anh_dai_dien"),
        "so_dia_diem": len(data.get("dia_diem", {})),
        "so_mon_an": len(data.get("mon_an", {})),
        "van_hoa": data.get("van_hoa", [])
    }

@app.get("/api/ai/mekong")
def api_random_mekong():
    # Đọc tham số count, mặc định 6
    try:
        count = int(request.args.get("count", 6))
    except ValueError:
        count = 6

    # Lọc những key miền Tây có thật trong dulieu
    available = [k for k in MEKONG_KEYS if k in dulieu]
    if not available:
        return jsonify({"error": "dulieu rỗng hoặc thiếu các tỉnh miền Tây"}), 500

    # Ràng buộc count hợp lệ
    count = max(1, min(count, len(available)))

    # Lấy ngẫu nhiên
    chosen_ids = random.sample(available, count)

    # Biến đổi dữ liệu trả ra
    results = [pick_fields(pid, dulieu[pid]) for pid in chosen_ids]

    return jsonify({
        "count": count,
        "ket_qua": results
    })

if __name__ == "__main__":
    # Chạy local: http://127.0.0.1:8000/api/ai/mekong?count=6
    app.run(host="0.0.0.0", port=8000, debug=True)
