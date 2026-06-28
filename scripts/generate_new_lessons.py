#!/usr/bin/env python3
"""Generate structured lesson data for lessons 7-9."""

import json
from pathlib import Path

LESSONS = [
    {
        "lesson_id": "delivery-installation-07",
        "title_en": "Delivery & Installation",
        "title_zh": "送货与安装",
        "description": "Mr. Zhang's sofa set arrives. The team delivers, assembles, and checks everything together.",
        "visual_style": "See style-guide.md for full consistency rules",
        "scenes": [
            {
                "id": 1,
                "image": "visuals/lesson07/scene-01.jpg",
                "title_en": "The Team Arrives",
                "title_zh": "送货团队到达",
                "description": "Li Wei and the delivery team arrive at Mr. Zhang's apartment.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Good morning, Mr. Zhang. We're here with your sofa set.",
                        "zh": "早上好，张先生。我们把您的沙发套装送来了。",
                        "vocab": ["sofa set"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Great, please come in. The elevator is just around the corner.",
                        "zh": "太好了，请进。电梯就在拐角处。",
                        "vocab": ["elevator", "around the corner"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Thank you. We'll be careful with the walls and floor.",
                        "zh": "谢谢。我们会小心墙面和地板的。",
                        "vocab": ["careful"]
                    }
                ]
            },
            {
                "id": 2,
                "image": "visuals/lesson07/scene-02.jpg",
                "title_en": "Unpacking in the Living Room",
                "title_zh": "在客厅拆包装",
                "description": "The team prepares the sofa in the living room.",
                "lines": [
                    {
                        "speaker": "Worker",
                        "role": "sales",
                        "en": "Where would you like the sofa, sir?",
                        "zh": "先生，您希望把沙发放在哪里？",
                        "vocab": ["would like"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Against that wall, facing the window.",
                        "zh": "靠那面墙，面向窗户。",
                        "vocab": ["against", "facing"]
                    },
                    {
                        "speaker": "Worker",
                        "role": "sales",
                        "en": "Understood. We'll remove the packaging first.",
                        "zh": "明白了。我们先拆掉包装。",
                        "vocab": ["packaging"]
                    }
                ]
            },
            {
                "id": 3,
                "image": "visuals/lesson07/scene-03.jpg",
                "title_en": "Assembling the Frame",
                "title_zh": "组装框架",
                "description": "The delivery team connects the sofa parts.",
                "lines": [
                    {
                        "speaker": "Worker",
                        "role": "sales",
                        "en": "The sofa comes in two parts. We need to connect them.",
                        "zh": "这款沙发分两部分。我们需要把它们连接起来。",
                        "vocab": ["comes in", "connect"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "How long does the assembly take?",
                        "zh": "组装需要多久？",
                        "vocab": ["assembly"]
                    },
                    {
                        "speaker": "Worker",
                        "role": "sales",
                        "en": "About fifteen minutes. The tools are in our van.",
                        "zh": "大约十五分钟。工具在我们的货车里。",
                        "vocab": ["van"]
                    }
                ]
            },
            {
                "id": 4,
                "image": "visuals/lesson07/scene-04.jpg",
                "title_en": "Checking the Position",
                "title_zh": "确认摆放位置",
                "description": "Li Wei confirms the sofa placement with Mr. Zhang.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Is this placement okay, Mr. Zhang?",
                        "zh": "张先生，这样摆放可以吗？",
                        "vocab": ["placement"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Could you move it a little to the left?",
                        "zh": "能往左移一点吗？",
                        "vocab": ["to the left"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Of course. Let me adjust it now.",
                        "zh": "当然可以。我现在调整一下。",
                        "vocab": ["adjust"]
                    }
                ]
            },
            {
                "id": 5,
                "image": "visuals/lesson07/scene-05.jpg",
                "title_en": "Inspecting for Damage",
                "title_zh": "检查损坏",
                "description": "Mr. Zhang checks the sofa condition carefully.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I don't see any scratches. The fabric looks perfect.",
                        "zh": "我没看到划痕。面料看起来很完美。",
                        "vocab": ["scratches", "fabric"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "We checked everything before leaving the showroom.",
                        "zh": "我们离开展厅前已经检查过所有东西了。",
                        "vocab": ["showroom"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Excellent. I'm very happy with it.",
                        "zh": "太好了。我非常满意。",
                        "vocab": ["happy with"]
                    }
                ]
            },
            {
                "id": 6,
                "image": "visuals/lesson07/scene-06.jpg",
                "title_en": "Signing the Delivery Note",
                "title_zh": "签收送货单",
                "description": "Mr. Zhang signs the delivery confirmation.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Please sign here to confirm delivery and installation.",
                        "zh": "请在这里签字确认送货和安装。",
                        "vocab": ["confirm", "delivery", "installation"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Sure. Thank you for your careful work.",
                        "zh": "好的。谢谢你们细心的工作。",
                        "vocab": ["careful"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "You're welcome. Enjoy your new sofa!",
                        "zh": "不客气。祝您享受新沙发！",
                        "vocab": ["Enjoy"]
                    }
                ]
            }
        ],
        "key_vocab_summary": [
            "sofa set", "elevator", "careful", "packaging", "assembly", "van",
            "placement", "adjust", "scratches", "confirm", "delivery", "installation"
        ]
    },
    {
        "lesson_id": "warranty-care-08",
        "title_en": "Warranty & Care",
        "title_zh": "保修与保养",
        "description": "Mr. Zhang calls Li Wei about a coffee stain and learns about warranty coverage and care tips.",
        "visual_style": "See style-guide.md for full consistency rules",
        "scenes": [
            {
                "id": 1,
                "image": "visuals/lesson08/scene-01.jpg",
                "title_en": "A Phone Call to the Showroom",
                "title_zh": "致电展厅",
                "description": "Mr. Zhang calls Li Wei about a stain on the sofa.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Hi Li Wei, I spilled coffee on the sofa. What should I do?",
                        "zh": "嗨李伟，我把咖啡洒在沙发上了。我该怎么办？",
                        "vocab": ["spilled"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Don't worry. Blot it gently with a clean cloth first.",
                        "zh": "别担心。先用干净的布轻轻吸干。",
                        "vocab": ["blot", "gently", "cloth"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Okay, I did that. Will it leave a stain?",
                        "zh": "好的，我做了。会留下污渍吗？",
                        "vocab": ["stain"]
                    }
                ]
            },
            {
                "id": 2,
                "image": "visuals/lesson08/scene-02.jpg",
                "title_en": "Cleaning Advice",
                "title_zh": "清洁建议",
                "description": "Li Wei gives Mr. Zhang simple cleaning instructions.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Use warm water and a little mild soap on the spot.",
                        "zh": "用温水和少量温和的肥皂处理污渍处。",
                        "vocab": ["mild soap", "spot"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Should I rub it hard?",
                        "zh": "我要用力擦吗？",
                        "vocab": ["rub"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "No, just dab it softly. Let it air dry.",
                        "zh": "不用，轻轻拍打就好。让它自然风干。",
                        "vocab": ["dab", "air dry"]
                    }
                ]
            },
            {
                "id": 3,
                "image": "visuals/lesson08/scene-03.jpg",
                "title_en": "Warranty Coverage",
                "title_zh": "保修范围",
                "description": "Mr. Zhang asks whether the stain is covered by warranty.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Is this kind of damage covered by the warranty?",
                        "zh": "这种损坏在保修范围内吗？",
                        "vocab": ["covered", "warranty"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Stains from daily use are not covered, but the fabric is stain-resistant.",
                        "zh": "日常使用的污渍不在保修范围内，但面料是防污的。",
                        "vocab": ["daily use", "stain-resistant"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I see. So I should clean it myself.",
                        "zh": "明白了。所以我得自己清理。",
                        "vocab": ["clean"]
                    }
                ]
            },
            {
                "id": 4,
                "image": "visuals/lesson08/scene-04.jpg",
                "title_en": "Professional Cleaning Service",
                "title_zh": "专业清洁服务",
                "description": "Li Wei introduces the showroom's cleaning service.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "We also offer a professional cleaning service twice a year.",
                        "zh": "我们还提供每年两次的专业清洁服务。",
                        "vocab": ["professional", "cleaning service"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "How much does it cost?",
                        "zh": "多少钱一次？",
                        "vocab": ["cost"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "It's free for the first year. After that, 300 RMB per visit.",
                        "zh": "第一年免费。之后每次300元。",
                        "vocab": ["per visit"]
                    }
                ]
            },
            {
                "id": 5,
                "image": "visuals/lesson08/scene-05.jpg",
                "title_en": "Scheduling a Cleaning",
                "title_zh": "预约清洁",
                "description": "Mr. Zhang books the free cleaning service.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I'd like to book the free cleaning next month.",
                        "zh": "我想预约下个月的免费清洁。",
                        "vocab": ["book"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Perfect. I'll arrange it for the first Saturday of next month.",
                        "zh": "好的。我安排在下个月第一个周六。",
                        "vocab": ["arrange"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "That works for me. Thank you.",
                        "zh": "那对我合适。谢谢。",
                        "vocab": ["works for me"]
                    }
                ]
            },
            {
                "id": 6,
                "image": "visuals/lesson08/scene-06.jpg",
                "title_en": "Care Tips",
                "title_zh": "保养建议",
                "description": "Li Wei shares daily care advice for the sofa.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Avoid direct sunlight and vacuum the sofa weekly.",
                        "zh": "避免阳光直射，每周用吸尘器清理沙发。",
                        "vocab": ["direct sunlight", "vacuum", "weekly"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Good tips. I'll take good care of it.",
                        "zh": "好建议。我会好好保养的。",
                        "vocab": ["take care of"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "If you have any questions, just call us anytime.",
                        "zh": "如果有任何问题，随时打电话给我们。",
                        "vocab": ["anytime"]
                    }
                ]
            }
        ],
        "key_vocab_summary": [
            "spilled", "blot", "gently", "stain", "mild soap", "dab", "air dry",
            "warranty", "daily use", "stain-resistant", "professional", "cleaning service",
            "book", "arrange", "direct sunlight", "vacuum", "take care of"
        ]
    },
    {
        "lesson_id": "bedroom-set-09",
        "title_en": "A New Order for the Bedroom",
        "title_zh": "卧室新订单",
        "description": "Mr. Zhang returns to buy a bedroom set and gets a bundle discount.",
        "visual_style": "See style-guide.md for full consistency rules",
        "scenes": [
            {
                "id": 1,
                "image": "visuals/lesson09/scene-01.jpg",
                "title_en": "Mr. Zhang Returns",
                "title_zh": "张先生再次光临",
                "description": "Mr. Zhang comes back to the showroom for bedroom furniture.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Welcome back, Mr. Zhang. How is the sofa?",
                        "zh": "欢迎再次光临，张先生。沙发怎么样？",
                        "vocab": ["Welcome back"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Very comfortable. Now I need a bedroom set.",
                        "zh": "非常舒服。现在我需要一套卧室家具。",
                        "vocab": ["bedroom set"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Wonderful. Let me show you our latest collection.",
                        "zh": "太好了。让我带您看看我们最新的系列。",
                        "vocab": ["collection"]
                    }
                ]
            },
            {
                "id": 2,
                "image": "visuals/lesson09/scene-02.jpg",
                "title_en": "Choosing a Bed Frame",
                "title_zh": "选择床架",
                "description": "Li Wei shows a solid wood bed frame.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "This king-size bed frame is solid walnut wood.",
                        "zh": "这款特大号床架是实心胡桃木的。",
                        "vocab": ["king-size", "walnut wood"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I like the color. Is it strong enough?",
                        "zh": "我喜欢这个颜色。它够结实吗？",
                        "vocab": ["strong enough"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Yes, it supports up to 300 kilograms.",
                        "zh": "是的，它可以承重高达300公斤。",
                        "vocab": ["supports", "kilograms"]
                    }
                ]
            },
            {
                "id": 3,
                "image": "visuals/lesson09/scene-03.jpg",
                "title_en": "Testing the Mattress",
                "title_zh": "试床垫",
                "description": "Mr. Zhang tries the mattress for comfort.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "This mattress feels firm but comfortable.",
                        "zh": "这个床垫感觉结实但舒适。",
                        "vocab": ["mattress", "firm"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "It has memory foam and pocket springs for back support.",
                        "zh": "它有记忆棉和独立袋装弹簧，可以支撑背部。",
                        "vocab": ["memory foam", "pocket springs", "back support"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Can I try lying on it?",
                        "zh": "我可以躺上去试试吗？",
                        "vocab": ["lying on"]
                    }
                ]
            },
            {
                "id": 4,
                "image": "visuals/lesson09/scene-04.jpg",
                "title_en": "Matching Nightstands",
                "title_zh": "配套床头柜",
                "description": "They look at nightstands that match the bed frame.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "These nightstands match the bed frame perfectly.",
                        "zh": "这些床头柜和床架完美搭配。",
                        "vocab": ["nightstands", "match", "perfectly"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "Do they have soft-close drawers?",
                        "zh": "它们的抽屉是缓冲关闭的吗？",
                        "vocab": ["soft-close", "drawers"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Yes, and the handles are brushed brass.",
                        "zh": "是的，把手是拉丝黄铜的。",
                        "vocab": ["handles", "brushed brass"]
                    }
                ]
            },
            {
                "id": 5,
                "image": "visuals/lesson09/scene-05.jpg",
                "title_en": "Wardrobe Options",
                "title_zh": "衣柜选择",
                "description": "Mr. Zhang asks about a wardrobe with sliding doors.",
                "lines": [
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "I also need a wardrobe with sliding doors.",
                        "zh": "我还需要一个推拉门衣柜。",
                        "vocab": ["wardrobe", "sliding doors"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "This one has a mirror and plenty of hanging space.",
                        "zh": "这款带镜子，还有很多挂衣空间。",
                        "vocab": ["plenty of", "hanging space"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "What are the dimensions?",
                        "zh": "尺寸是多少？",
                        "vocab": ["dimensions"]
                    }
                ]
            },
            {
                "id": 6,
                "image": "visuals/lesson09/scene-06.jpg",
                "title_en": "Bundle Discount",
                "title_zh": "套餐优惠",
                "description": "Li Wei offers a discount for buying the full bedroom set.",
                "lines": [
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "If you buy the bed, two nightstands and wardrobe together, you get 20% off.",
                        "zh": "如果您一起购买床、两个床头柜和衣柜，可以享受八折优惠。",
                        "vocab": ["together", "20% off"]
                    },
                    {
                        "speaker": "Mr. Zhang",
                        "role": "customer",
                        "en": "That's a great deal. I'll take the whole set.",
                        "zh": "真划算。我要整套。",
                        "vocab": ["great deal", "whole set"]
                    },
                    {
                        "speaker": "Li Wei",
                        "role": "sales",
                        "en": "Thank you. I'll prepare the contract for you.",
                        "zh": "谢谢。我为您准备合同。",
                        "vocab": ["contract"]
                    }
                ]
            }
        ],
        "key_vocab_summary": [
            "bedroom set", "collection", "king-size", "walnut wood", "mattress",
            "memory foam", "pocket springs", "nightstands", "soft-close", "drawers",
            "brushed brass", "wardrobe", "sliding doors", "hanging space", "dimensions",
            "20% off", "great deal", "whole set", "contract"
        ]
    }
]


def main():
    mappings = {
        "delivery-installation-07": "lesson-07-data.json",
        "warranty-care-08": "lesson-08-data.json",
        "bedroom-set-09": "lesson-09-data.json",
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
