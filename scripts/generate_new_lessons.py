#!/usr/bin/env python3
"""Generate structured lesson data for lessons 2-4 based on OCR content."""

import json
from pathlib import Path

LESSONS = [
    {
        "lesson_id": "choosing-sofa-02",
        "title_en": "Choosing the Perfect Sofa",
        "title_zh": "挑选理想沙发",
        "description": "Mr. Zhang returns to the showroom and learns about materials, colors, and sizes before choosing a sofa.",
        "visual_style": "See style-guide.md for full consistency rules",
        "scenes": [
            {
                "id": 1,
                "image": "visuals/lesson02/scene-01.jpg",
                "title_en": "Welcome Back",
                "title_zh": "欢迎回头客",
                "description": "Mr. Zhang comes back to look at sofas.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Welcome back, Mr. Zhang. What would you like to see today?",
                        "zh": "欢迎再次光临，张先生。今天想看些什么？",
                        "vocab": ["Welcome back"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I'd like to see some sofas. What materials do you have?",
                        "zh": "我想看看沙发。你们有什么材质的？",
                        "vocab": ["materials"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "We have fabric, leather, genuine leather and solid wood frames.",
                        "zh": "我们有布艺、皮革、真皮和实木框架的。",
                        "vocab": ["fabric", "genuine leather", "solid wood"]
                    }
                ]
            },
            {
                "id": 2,
                "image": "visuals/lesson02/scene-02.jpg",
                "title_en": "Choosing the Material",
                "title_zh": "选择材质",
                "description": "Li Wei explains the differences between materials.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "What is this sofa made of?",
                        "zh": "这个沙发是什么材质的？",
                        "vocab": ["made of"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "It's made of real leather, so it's very durable.",
                        "zh": "这是用真皮做的，所以非常耐用。",
                        "vocab": ["real leather", "durable"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Do you have fabric sofas too?",
                        "zh": "你们也有布艺沙发吗？",
                        "vocab": ["fabric sofas"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Yes. This fabric sofa is soft and easy to clean.",
                        "zh": "有的。这款布艺沙发柔软且容易清洁。",
                        "vocab": ["soft", "easy to clean"]
                    }
                ]
            },
            {
                "id": 3,
                "image": "visuals/lesson02/scene-03.jpg",
                "title_en": "Picking a Color",
                "title_zh": "挑选颜色",
                "description": "They look at color swatches for the sofa.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "How many colors do you have for this design?",
                        "zh": "这款设计有多少种颜色？",
                        "vocab": ["design"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "We have red, white, black, brown and beige.",
                        "zh": "我们有红色、白色、黑色、棕色和米色。",
                        "vocab": ["beige"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "I like the brown one. Can you customize the color?",
                        "zh": "我喜欢棕色的。可以定制颜色吗？",
                        "vocab": ["customize"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Of course. We can make it in light brown if you prefer.",
                        "zh": "当然可以。如果您喜欢，我们可以做成浅棕色。",
                        "vocab": ["light brown"]
                    }
                ]
            },
            {
                "id": 4,
                "image": "visuals/lesson02/scene-04.jpg",
                "title_en": "Checking the Size",
                "title_zh": "确认尺寸",
                "description": "Mr. Zhang asks about the sofa dimensions.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Can you tell me the size of this sofa?",
                        "zh": "能告诉我这个沙发的尺寸吗？",
                        "vocab": ["size"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "This three-seater is 2.2 meters long, 95 centimeters deep and 85 centimeters high.",
                        "zh": "这款三人沙发长2.2米，深95厘米，高85厘米。",
                        "vocab": ["three-seater", "meters", "centimeters"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Do you have a bigger size?",
                        "zh": "你们有更大的尺寸吗？",
                        "vocab": ["bigger size"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Yes, we also have a king-size sofa that is 2.4 meters long.",
                        "zh": "有的，我们还有一款特大号沙发，长2.4米。",
                        "vocab": ["king-size"]
                    }
                ]
            },
            {
                "id": 5,
                "image": "visuals/lesson02/scene-05.jpg",
                "title_en": "Trying the Sofa",
                "title_zh": "试坐沙发",
                "description": "Mr. Zhang sits on the sofa to test comfort.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Would you like to sit down and try it?",
                        "zh": "您要坐下来试试吗？",
                        "vocab": ["try it"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "It's quite comfortable. The cushions are firm but soft.",
                        "zh": "相当舒服。靠垫结实又柔软。",
                        "vocab": ["comfortable", "cushions", "firm"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "This model sells very well because of its design.",
                        "zh": "这款因为设计好，卖得很不错。",
                        "vocab": ["sells very well"]
                    }
                ]
            },
            {
                "id": 6,
                "image": "visuals/lesson02/scene-06.jpg",
                "title_en": "A Preliminary Decision",
                "title_zh": "初步决定",
                "description": "Mr. Zhang decides on the material and color.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I like the genuine leather sofa in light brown, 2.4 meters.",
                        "zh": "我喜欢浅棕色2.4米的真皮沙发。",
                        "vocab": ["genuine leather"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Great choice. Let me write down the details for you.",
                        "zh": "好选择。让我把细节记下来。",
                        "vocab": ["write down", "details"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Thank you. I'll think about it and come back tomorrow.",
                        "zh": "谢谢。我考虑一下，明天再来。",
                        "vocab": ["think about"]
                    }
                ]
            }
        ],
        "key_vocab_summary": [
            "materials", "fabric", "genuine leather", "solid wood", "made of",
            "real leather", "durable", "soft", "easy to clean", "design",
            "customize", "light brown", "size", "three-seater", "meters",
            "centimeters", "king-size", "comfortable", "cushions", "firm",
            "sells very well", "write down", "details", "think about"
        ]
    },
    {
        "lesson_id": "negotiating-order-03",
        "title_en": "Negotiating a Big Order",
        "title_zh": "大宗订单谈判",
        "description": "A business customer wants to order office furniture. They discuss quantity, quality, and price.",
        "visual_style": "See style-guide.md for full consistency rules",
        "scenes": [
            {
                "id": 1,
                "image": "visuals/lesson03/scene-01.jpg",
                "title_en": "A New Customer",
                "title_zh": "新客户",
                "description": "A business customer arrives to buy office furniture.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Good morning. Welcome to our shop. What can I do for you?",
                        "zh": "早上好，欢迎光临。有什么可以帮到您的？",
                        "vocab": ["Good morning"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "I need to buy some office furniture. Can you show me around?",
                        "zh": "我需要买一些办公家具。能带我看看吗？",
                        "vocab": ["office furniture", "show me around"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Sure. These are our office tables and computer desks.",
                        "zh": "当然。这些是我们的办公台和电脑桌。",
                        "vocab": ["office tables", "computer desks"]
                    }
                ]
            },
            {
                "id": 2,
                "image": "visuals/lesson03/scene-02.jpg",
                "title_en": "Choosing Products",
                "title_zh": "选择产品",
                "description": "The customer picks computer desks and chairs.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "I want to buy this computer desk. What is it made of?",
                        "zh": "我想买这张电脑桌。它是什么材质的？",
                        "vocab": ["computer desk"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "This one is made of MDF, but we have the same style in plywood.",
                        "zh": "这款是中纤板的，但我们有同款胶合板的。",
                        "vocab": ["MDF", "plywood"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "I also need boss chairs. What colors do you have?",
                        "zh": "我还需要老板椅。有什么颜色？",
                        "vocab": ["boss chairs"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "We have blue, black and red. You can choose leather, fabric or PU leather.",
                        "zh": "有蓝色、黑色和红色。您可以选择皮革、布艺或PU皮。",
                        "vocab": ["PU leather"]
                    }
                ]
            },
            {
                "id": 3,
                "image": "visuals/lesson03/scene-03.jpg",
                "title_en": "Talking About Quantity",
                "title_zh": "谈论数量",
                "description": "They confirm how many pieces the customer wants.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "How many desks and chairs do you want to buy?",
                        "zh": "您想买多少张桌子和椅子？",
                        "vocab": ["How many"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "I want 100 computer desks and 100 boss chairs.",
                        "zh": "我要100张电脑桌和100张老板椅。",
                        "vocab": ["computer desks"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "That's a large order. We can offer a better price.",
                        "zh": "这是大宗订单。我们可以给更优惠的价格。",
                        "vocab": ["large order", "better price"]
                    }
                ]
            },
            {
                "id": 4,
                "image": "visuals/lesson03/scene-04.jpg",
                "title_en": "Quality Guarantee",
                "title_zh": "质量保证",
                "description": "The customer asks about quality and durability.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "How long can this chair last?",
                        "zh": "这把椅子能用多久？",
                        "vocab": ["last"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "It can last for at least ten years if you use it in the right way.",
                        "zh": "如果使用得当，至少可以用十年。",
                        "vocab": ["at least", "ten years"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Your quality is the best among the suppliers I have visited.",
                        "zh": "在我参观过的供应商中，你们的质量是最好的。",
                        "vocab": ["quality", "suppliers"]
                    }
                ]
            },
            {
                "id": 5,
                "image": "visuals/lesson03/scene-05.jpg",
                "title_en": "Price Negotiation",
                "title_zh": "价格谈判",
                "description": "They negotiate the price for the large order.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "The desk is 700 RMB and the chair is 500 RMB.",
                        "zh": "桌子700元，椅子500元。",
                        "vocab": ["RMB"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "This price is too high for such a big order. How about 600 for the desk and 400 for the chair?",
                        "zh": "这么大的订单，这个价格太高了。桌子600、椅子400怎么样？",
                        "vocab": ["big order"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Sorry, that's lower than our wholesale price. 650 and 450 is the best we can do.",
                        "zh": "抱歉，这低于我们的批发价。650和450是我们能给的最低价。",
                        "vocab": ["wholesale price"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "OK, then we have a deal.",
                        "zh": "好的，成交。",
                        "vocab": ["deal"]
                    }
                ]
            },
            {
                "id": 6,
                "image": "visuals/lesson03/scene-06.jpg",
                "title_en": "Next Steps",
                "title_zh": "下一步",
                "description": "They agree to visit the factory before finalizing.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Can I visit your factory before I place the order?",
                        "zh": "下单前我可以参观你们的工厂吗？",
                        "vocab": ["place the order"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Of course. We can pick you up anytime.",
                        "zh": "当然可以。我们随时可以接送。",
                        "vocab": ["pick you up", "anytime"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "How about tomorrow morning?",
                        "zh": "明天上午怎么样？",
                        "vocab": ["How about"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Tomorrow morning is fine. I'll show you around our workshop.",
                        "zh": "明天上午可以。我带您参观我们的车间。",
                        "vocab": ["show you around", "workshop"]
                    }
                ]
            }
        ],
        "key_vocab_summary": [
            "office furniture", "show me around", "office tables", "computer desks",
            "MDF", "plywood", "boss chairs", "PU leather", "How many", "large order",
            "better price", "last", "at least", "ten years", "quality", "suppliers",
            "big order", "wholesale price", "deal", "place the order", "pick you up",
            "anytime", "show you around", "workshop"
        ]
    },
    {
        "lesson_id": "factory-visit-04",
        "title_en": "Factory Visit and Final Deal",
        "title_zh": "参观工厂与最终成交",
        "description": "The customer visits the factory, confirms the order, discusses payment, and arranges delivery.",
        "visual_style": "See style-guide.md for full consistency rules",
        "scenes": [
            {
                "id": 1,
                "image": "visuals/lesson04/scene-01.jpg",
                "title_en": "Arriving at the Factory",
                "title_zh": "到达工厂",
                "description": "Li Wei picks up the customer and shows the factory.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Welcome to our factory. Let me show you around.",
                        "zh": "欢迎来到我们的工厂。让我带您参观一下。",
                        "vocab": ["factory", "show you around"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Thank you. How big is your factory?",
                        "zh": "谢谢。你们的工厂多大？",
                        "vocab": ["How big"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "It covers about 10,000 square meters. We have about 120 workers.",
                        "zh": "大约占地一万平米。我们有大约120名工人。",
                        "vocab": ["square meters", "workers"]
                    }
                ]
            },
            {
                "id": 2,
                "image": "visuals/lesson04/scene-02.jpg",
                "title_en": "The Workshop",
                "title_zh": "车间",
                "description": "They visit the production workshop.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Can we have a look at the workshop?",
                        "zh": "我们可以看一下车间吗？",
                        "vocab": ["workshop"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Of course. This way please. This is where we make the frames.",
                        "zh": "当然。请这边走。这是我们做框架的地方。",
                        "vocab": ["frames"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Your company is very big. I'm impressed.",
                        "zh": "你们公司很大。我印象深刻。",
                        "vocab": ["impressed"]
                    }
                ]
            },
            {
                "id": 3,
                "image": "visuals/lesson04/scene-03.jpg",
                "title_en": "Placing the Order",
                "title_zh": "下订单",
                "description": "The customer decides to place the order after the visit.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "I'm satisfied with your factory. Let's make the order now.",
                        "zh": "我对你们的工厂很满意。我们现在下单吧。",
                        "vocab": ["satisfied", "make the order"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Great. So it's 100 desks and 100 chairs. The total is 110,000 RMB.",
                        "zh": "太好了。那就是100张桌子和100张椅子。总共11万元。",
                        "vocab": ["total"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Can you deliver in two weeks?",
                        "zh": "你们能在两周内交货吗？",
                        "vocab": ["deliver", "in two weeks"]
                    }
                ]
            },
            {
                "id": 4,
                "image": "visuals/lesson04/scene-04.jpg",
                "title_en": "Payment Terms",
                "title_zh": "付款条款",
                "description": "They discuss deposit and balance payment.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "You can pay 30% deposit now and the balance before delivery.",
                        "zh": "您可以现在付30%定金，余款在发货前付清。",
                        "vocab": ["deposit", "balance", "before delivery"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Do you accept T/T or card?",
                        "zh": "你们接受转账还是刷卡？",
                        "vocab": ["T/T", "card"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Both are fine. The deposit is 33,000 RMB.",
                        "zh": "都可以。定金是3万3千元。",
                        "vocab": ["deposit"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "No problem. I'll pay by card now.",
                        "zh": "没问题。我现在刷卡。",
                        "vocab": ["pay by card"]
                    }
                ]
            },
            {
                "id": 5,
                "image": "visuals/lesson04/scene-05.jpg",
                "title_en": "Packing and Volume",
                "title_zh": "包装与体积",
                "description": "They confirm packing details and shipping volume.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "How do you pack the furniture?",
                        "zh": "你们怎么包装家具？",
                        "vocab": ["pack"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Ordinary packing is carton with sponge. Wooden crates are available for extra cost.",
                        "zh": "普通包装是纸箱加海绵。木箱需要额外付费。",
                        "vocab": ["carton", "sponge", "wooden crates"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "What is the total volume?",
                        "zh": "总体积是多少？",
                        "vocab": ["volume"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "It's about 35 CBM in total. A 40 HQ container holds about 68 CBM.",
                        "zh": "总共大约35立方米。40尺高柜大约能装68立方米。",
                        "vocab": ["CBM", "40 HQ container"]
                    }
                ]
            },
            {
                "id": 6,
                "image": "visuals/lesson04/scene-06.jpg",
                "title_en": "Delivery Arrangement",
                "title_zh": "交货安排",
                "description": "They finalize the delivery schedule and say goodbye.",
                "lines": [
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "When can you deliver the goods?",
                        "zh": "你们什么时候可以发货？",
                        "vocab": ["deliver the goods"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "In two weeks. We will load the container next Friday.",
                        "zh": "两周后。我们下周五装柜。",
                        "vocab": ["load the container"]
                    },
                    {
                        "speaker": "Customer",
                        "role": "customer",
                        "en": "Can you make it one week? We need them urgently.",
                        "zh": "能缩短到一周吗？我们急需。",
                        "vocab": ["urgently"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "We are very busy, but we will try our best.",
                        "zh": "我们很忙，但会尽力。",
                        "vocab": ["try our best"]
                    }
                ]
            }
        ],
        "key_vocab_summary": [
            "factory", "show you around", "square meters", "workers", "workshop",
            "frames", "impressed", "satisfied", "make the order", "total",
            "deliver", "in two weeks", "deposit", "balance", "before delivery",
            "T/T", "card", "pay by card", "pack", "carton", "sponge",
            "wooden crates", "volume", "CBM", "40 HQ container", "deliver the goods",
            "load the container", "urgently", "try our best"
        ]
    }
]


def main():
    mappings = {
        "choosing-sofa-02": "lesson-02-data.json",
        "negotiating-order-03": "lesson-03-data.json",
        "factory-visit-04": "lesson-04-data.json",
    }

    for lesson in LESSONS:
        filename = mappings[lesson["lesson_id"]]
        Path(filename).write_text(json.dumps(lesson, ensure_ascii=False, indent=2) + "\n")
        (Path("web") / filename).write_text(
            json.dumps(lesson, ensure_ascii=False, indent=2) + "\n"
        )
        print(f"Wrote {filename} and web/{filename}")


if __name__ == "__main__":
    main()
