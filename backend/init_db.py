from app.database import engine, Base, SessionLocal
from app.models.question import Category, KnowledgePoint, Question
import json

def init_db():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("数据库已初始化，跳过")
            return
        
        # 创建科目
        categories = [
            Category(name="数学", description="数学学科，包含代数、几何、统计等内容"),
            Category(name="英语", description="英语学科，包含语法、词汇、阅读等内容"),
            Category(name="物理", description="物理学科，包含力学、电学、光学等内容"),
            Category(name="化学", description="化学学科，包含无机化学、有机化学等内容")
        ]
        db.add_all(categories)
        db.commit()
        
        # 创建知识点
        knowledge_points = [
            # 数学知识点 (1-5)
            KnowledgePoint(name="集合", category_id=1, description="集合的基本概念和运算"),
            KnowledgePoint(name="函数", category_id=1, description="函数的性质和图像"),
            KnowledgePoint(name="三角函数", category_id=1, description="三角函数的定义和性质"),
            KnowledgePoint(name="数列", category_id=1, description="等差数列和等比数列"),
            KnowledgePoint(name="立体几何", category_id=1, description="空间几何体的性质"),
            
            # 英语知识点 (6-9)
            KnowledgePoint(name="时态", category_id=2, description="英语时态的用法"),
            KnowledgePoint(name="虚拟语气", category_id=2, description="虚拟语气的三种情况"),
            KnowledgePoint(name="定语从句", category_id=2, description="定语从句的引导词和用法"),
            KnowledgePoint(name="非谓语动词", category_id=2, description="不定式、动名词、分词的用法"),
            
            # 物理知识点 (10-12)
            KnowledgePoint(name="牛顿定律", category_id=3, description="牛顿三大定律"),
            KnowledgePoint(name="电磁感应", category_id=3, description="电磁感应现象"),
            KnowledgePoint(name="动量守恒", category_id=3, description="动量守恒定律"),
            
            # 化学知识点 (13-15)
            KnowledgePoint(name="化学平衡", category_id=4, description="化学平衡原理"),
            KnowledgePoint(name="氧化还原", category_id=4, description="氧化还原反应"),
            KnowledgePoint(name="有机化学", category_id=4, description="有机化合物的性质")
        ]
        db.add_all(knowledge_points)
        db.commit()
        
        # 创建题目 - 数学（集合）
        math_set_questions = [
            Question(
                content="已知集合A={1,2,3}，B={2,3,4}，则A∩B=",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "{1,2,3,4}"},
                    {"label": "B", "content": "{2,3}"},
                    {"label": "C", "content": "{1,4}"},
                    {"label": "D", "content": "∅"}
                ]),
                answer="B",
                explanation="交集是两个集合共有的元素组成的集合，A和B共有的元素是2和3。",
                category_id=1, knowledge_point_id=1
            ),
            Question(
                content="已知集合A={1,2,3,4}，B={3,4,5,6}，则A∪B=",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "{3,4}"},
                    {"label": "B", "content": "{1,2,5,6}"},
                    {"label": "C", "content": "{1,2,3,4,5,6}"},
                    {"label": "D", "content": "{1,2,3,4}"}
                ]),
                answer="C",
                explanation="并集是两个集合所有元素组成的集合，A∪B={1,2,3,4,5,6}。",
                category_id=1, knowledge_point_id=1
            ),
            Question(
                content="设全集U={1,2,3,4,5}，A={1,3,5}，则∁UA=",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "{1,3,5}"},
                    {"label": "B", "content": "{2,4}"},
                    {"label": "C", "content": "{1,2,3,4,5}"},
                    {"label": "D", "content": "∅"}
                ]),
                answer="B",
                explanation="补集是全集中不属于A的元素组成的集合，∁UA={2,4}。",
                category_id=1, knowledge_point_id=1
            ),
            Question(
                content="集合{a,b}的子集个数为",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "2"},
                    {"label": "B", "content": "3"},
                    {"label": "C", "content": "4"},
                    {"label": "D", "content": "8"}
                ]),
                answer="C",
                explanation="含有n个元素的集合有2^n个子集，{a,b}有2^2=4个子集：∅,{a},{b},{a,b}。",
                category_id=1, knowledge_point_id=1
            ),
        ]
        
        # 创建题目 - 数学（函数）
        math_func_questions = [
            Question(
                content="函数f(x)=x²-2x+1的最小值为",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "-1"},
                    {"label": "B", "content": "0"},
                    {"label": "C", "content": "1"},
                    {"label": "D", "content": "2"}
                ]),
                answer="B",
                explanation="f(x)=(x-1)²≥0，当x=1时取最小值0。",
                category_id=1, knowledge_point_id=2
            ),
            Question(
                content="函数f(x)=2x+1在R上是",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "增函数"},
                    {"label": "B", "content": "减函数"},
                    {"label": "C", "content": "先增后减"},
                    {"label": "D", "content": "先减后增"}
                ]),
                answer="A",
                explanation="一次函数f(x)=kx+b，当k>0时是增函数，k=2>0，所以是增函数。",
                category_id=1, knowledge_point_id=2
            ),
            Question(
                content="若f(x)=x²，则f(-2)=",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "-4"},
                    {"label": "B", "content": "4"},
                    {"label": "C", "content": "-2"},
                    {"label": "D", "content": "2"}
                ]),
                answer="B",
                explanation="f(-2)=(-2)²=4。",
                category_id=1, knowledge_point_id=2
            ),
            Question(
                content="函数y=log₂x的定义域为",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "R"},
                    {"label": "B", "content": "(0,+∞)"},
                    {"label": "C", "content": "[0,+∞)"},
                    {"label": "D", "content": "(-∞,0)"}
                ]),
                answer="B",
                explanation="对数函数的真数必须大于0，所以定义域为(0,+∞)。",
                category_id=1, knowledge_point_id=2
            ),
        ]
        
        # 创建题目 - 数学（三角函数）
        math_trig_questions = [
            Question(
                content="sin30°的值为",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "1/2"},
                    {"label": "B", "content": "√2/2"},
                    {"label": "C", "content": "√3/2"},
                    {"label": "D", "content": "1"}
                ]),
                answer="A",
                explanation="sin30°=1/2，这是特殊角的三角函数值。",
                category_id=1, knowledge_point_id=3
            ),
            Question(
                content="cos60°的值为",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "1/2"},
                    {"label": "B", "content": "√2/2"},
                    {"label": "C", "content": "√3/2"},
                    {"label": "D", "content": "0"}
                ]),
                answer="A",
                explanation="cos60°=1/2，这是特殊角的三角函数值。",
                category_id=1, knowledge_point_id=3
            ),
            Question(
                content="tan45°的值为",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "0"},
                    {"label": "B", "content": "1"},
                    {"label": "C", "content": "√3"},
                    {"label": "D", "content": "不存在"}
                ]),
                answer="B",
                explanation="tan45°=1，这是特殊角的三角函数值。",
                category_id=1, knowledge_point_id=3
            ),
        ]
        
        # 创建题目 - 数学（数列）
        math_seq_questions = [
            Question(
                content="等差数列{an}中，a1=1，d=2，则a10=",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "17"},
                    {"label": "B", "content": "19"},
                    {"label": "C", "content": "21"},
                    {"label": "D", "content": "23"}
                ]),
                answer="B",
                explanation="等差数列通项公式：an=a1+(n-1)d，所以a10=1+(10-1)×2=19。",
                category_id=1, knowledge_point_id=4
            ),
            Question(
                content="等比数列{an}中，a1=1，q=2，则a5=",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "8"},
                    {"label": "B", "content": "16"},
                    {"label": "C", "content": "32"},
                    {"label": "D", "content": "64"}
                ]),
                answer="B",
                explanation="等比数列通项公式：an=a1×q^(n-1)，所以a5=1×2^4=16。",
                category_id=1, knowledge_point_id=4
            ),
            Question(
                content="数列1,3,5,7,9,...的通项公式为",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "an=n"},
                    {"label": "B", "content": "an=2n-1"},
                    {"label": "C", "content": "an=2n+1"},
                    {"label": "D", "content": "an=n+1"}
                ]),
                answer="B",
                explanation="这是一个首项为1，公差为2的等差数列，通项公式为an=1+(n-1)×2=2n-1。",
                category_id=1, knowledge_point_id=4
            ),
        ]
        
        # 创建题目 - 英语（时态）
        eng_tense_questions = [
            Question(
                content="I ___ to school by bus every day.",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "go"},
                    {"label": "B", "content": "goes"},
                    {"label": "C", "content": "going"},
                    {"label": "D", "content": "went"}
                ]),
                answer="A",
                explanation="every day表示经常性动作，用一般现在时。主语是I，动词用原形go。",
                category_id=2, knowledge_point_id=6
            ),
            Question(
                content="She ___ dinner when I called her.",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "cooks"},
                    {"label": "B", "content": "cooked"},
                    {"label": "C", "content": "was cooking"},
                    {"label": "D", "content": "has cooked"}
                ]),
                answer="C",
                explanation="when I called表示过去某一时刻，正在发生的动作用过去进行时was cooking。",
                category_id=2, knowledge_point_id=6
            ),
            Question(
                content="He ___ already ___ his homework.",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "has, finished"},
                    {"label": "B", "content": "have, finished"},
                    {"label": "C", "content": "had, finished"},
                    {"label": "D", "content": "was, finishing"}
                ]),
                answer="A",
                explanation="already常与现在完成时连用，主语He是第三人称单数，用has finished。",
                category_id=2, knowledge_point_id=6
            ),
            Question(
                content="I ___ this book last week.",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "read"},
                    {"label": "B", "content": "reads"},
                    {"label": "C", "content": "reading"},
                    {"label": "D", "content": "have read"}
                ]),
                answer="A",
                explanation="last week表示过去时间，用一般过去时。read的过去式还是read。",
                category_id=2, knowledge_point_id=6
            ),
        ]
        
        # 创建题目 - 英语（虚拟语气）
        eng_subjunctive_questions = [
            Question(
                content="If I ___ you, I would study harder.",
                question_type="single", difficulty="hard",
                options=json.dumps([
                    {"label": "A", "content": "am"},
                    {"label": "B", "content": "was"},
                    {"label": "C", "content": "were"},
                    {"label": "D", "content": "be"}
                ]),
                answer="C",
                explanation="虚拟语气中，be动词统一用were。",
                category_id=2, knowledge_point_id=7
            ),
            Question(
                content="I wish I ___ a bird.",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "am"},
                    {"label": "B", "content": "was"},
                    {"label": "C", "content": "were"},
                    {"label": "D", "content": "be"}
                ]),
                answer="C",
                explanation="wish后面的宾语从句用虚拟语气，be动词用were。",
                category_id=2, knowledge_point_id=7
            ),
        ]
        
        # 创建题目 - 英语（定语从句）
        eng_clause_questions = [
            Question(
                content="The book ___ by him last year is very popular.",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "wrote"},
                    {"label": "B", "content": "writing"},
                    {"label": "C", "content": "written"},
                    {"label": "D", "content": "was written"}
                ]),
                answer="C",
                explanation="过去分词作定语，表示被动和完成。",
                category_id=2, knowledge_point_id=9
            ),
            Question(
                content="The man ___ is standing there is my teacher.",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "who"},
                    {"label": "B", "content": "which"},
                    {"label": "C", "content": "whom"},
                    {"label": "D", "content": "whose"}
                ]),
                answer="A",
                explanation="先行词是人，在从句中作主语，用who引导。",
                category_id=2, knowledge_point_id=8
            ),
            Question(
                content="This is the house ___ I lived last year.",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "which"},
                    {"label": "B", "content": "where"},
                    {"label": "C", "content": "that"},
                    {"label": "D", "content": "when"}
                ]),
                answer="B",
                explanation="先行词是地点，在从句中作地点状语，用where引导。",
                category_id=2, knowledge_point_id=8
            ),
        ]
        
        # 创建题目 - 物理（牛顿定律）
        phy_newton_questions = [
            Question(
                content="力是改变物体运动状态的原因",
                question_type="judge", difficulty="easy",
                options=None,
                answer="正确",
                explanation="根据牛顿第一定律，力是改变物体运动状态的原因，而不是维持物体运动的原因。",
                category_id=3, knowledge_point_id=10
            ),
            Question(
                content="牛顿第二定律的表达式为",
                question_type="single", difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "F=ma"},
                    {"label": "B", "content": "F=mv"},
                    {"label": "C", "content": "F=mg"},
                    {"label": "D", "content": "F=1/2mv²"}
                ]),
                answer="A",
                explanation="牛顿第二定律：物体加速度的大小与作用力成正比，与质量成反比，F=ma。",
                category_id=3, knowledge_point_id=10
            ),
            Question(
                content="一个物体受到的合力为零，则该物体",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "一定静止"},
                    {"label": "B", "content": "一定做匀速直线运动"},
                    {"label": "C", "content": "可能静止或做匀速直线运动"},
                    {"label": "D", "content": "一定做加速运动"}
                ]),
                answer="C",
                explanation="根据牛顿第一定律，合力为零时，物体保持静止或匀速直线运动状态。",
                category_id=3, knowledge_point_id=10
            ),
            Question(
                content="牛顿第三定律指出，作用力与反作用力",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "大小相等，方向相同"},
                    {"label": "B", "content": "大小不等，方向相反"},
                    {"label": "C", "content": "大小相等，方向相反，作用在同一直线上"},
                    {"label": "D", "content": "大小相等，方向相反，作用在同一物体上"}
                ]),
                answer="C",
                explanation="牛顿第三定律：作用力与反作用力大小相等，方向相反，作用在同一直线上，分别作用在两个物体上。",
                category_id=3, knowledge_point_id=10
            ),
        ]
        
        # 创建题目 - 物理（电磁感应）
        phy_em_questions = [
            Question(
                content="下列关于电磁感应的说法正确的是",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "感应电流的磁场总是阻碍原磁场的变化"},
                    {"label": "B", "content": "感应电流的磁场总是与原磁场方向相反"},
                    {"label": "C", "content": "感应电流的磁场总是促进原磁场的变化"},
                    {"label": "D", "content": "感应电流的磁场方向与原磁场方向无关"}
                ]),
                answer="A",
                explanation="楞次定律：感应电流的磁场总是阻碍引起感应电流的磁通量的变化。",
                category_id=3, knowledge_point_id=11
            ),
            Question(
                content="闭合电路中产生感应电流的条件是",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "电路中有磁通量"},
                    {"label": "B", "content": "磁通量发生变化"},
                    {"label": "C", "content": "电路中有磁场"},
                    {"label": "D", "content": "电路中有电源"}
                ]),
                answer="B",
                explanation="闭合电路中产生感应电流的条件是：穿过闭合电路的磁通量发生变化。",
                category_id=3, knowledge_point_id=11
            ),
        ]
        
        # 创建题目 - 化学（氧化还原）
        chem_redox_questions = [
            Question(
                content="下列反应属于氧化还原反应的是",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "CaO + H₂O = Ca(OH)₂"},
                    {"label": "B", "content": "2Na + 2H₂O = 2NaOH + H₂↑"},
                    {"label": "C", "content": "CaCO₃ = CaO + CO₂↑"},
                    {"label": "D", "content": "NaOH + HCl = NaCl + H₂O"}
                ]),
                answer="B",
                explanation="氧化还原反应的特征是元素化合价发生变化。Na从0价变为+1价，H从+1价变为0价。",
                category_id=4, knowledge_point_id=14
            ),
            Question(
                content="在氧化还原反应中，氧化剂",
                question_type="single", difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "得到电子，化合价升高"},
                    {"label": "B", "content": "失去电子，化合价降低"},
                    {"label": "C", "content": "得到电子，化合价降低"},
                    {"label": "D", "content": "失去电子，化合价升高"}
                ]),
                answer="C",
                explanation="氧化剂得到电子，化合价降低，被还原。",
                category_id=4, knowledge_point_id=14
            ),
        ]
        
        # 创建题目 - 化学（化学平衡）
        chem_balance_questions = [
            Question(
                content="化学平衡常数K只与温度有关",
                question_type="judge", difficulty="medium",
                options=None,
                answer="正确",
                explanation="化学平衡常数K只与温度有关，与浓度、压强等因素无关。",
                category_id=4, knowledge_point_id=13
            ),
            Question(
                content="下列关于化学平衡的说法正确的是",
                question_type="single", difficulty="hard",
                options=json.dumps([
                    {"label": "A", "content": "化学平衡是动态平衡"},
                    {"label": "B", "content": "达到平衡时正反应速率等于零"},
                    {"label": "C", "content": "达到平衡时各物质浓度相等"},
                    {"label": "D", "content": "达到平衡时反应停止"}
                ]),
                answer="A",
                explanation="化学平衡是动态平衡，正逆反应速率相等但不为零，各物质浓度保持不变。",
                category_id=4, knowledge_point_id=13
            ),
        ]
        
        # 合并所有题目
        all_questions = (
            math_set_questions +
            math_func_questions +
            math_trig_questions +
            math_seq_questions +
            eng_tense_questions +
            eng_subjunctive_questions +
            eng_clause_questions +
            phy_newton_questions +
            phy_em_questions +
            chem_redox_questions +
            chem_balance_questions
        )
        
        db.add_all(all_questions)
        db.commit()
        
        print("=" * 50)
        print("数据库初始化成功！")
        print("=" * 50)
        print(f"创建了 {len(categories)} 个科目：数学、英语、物理、化学")
        print(f"创建了 {len(knowledge_points)} 个知识点")
        print(f"创建了 {len(all_questions)} 道题目")
        print("-" * 50)
        print("题目分布：")
        print(f"  数学集合：{len(math_set_questions)} 道")
        print(f"  数学函数：{len(math_func_questions)} 道")
        print(f"  数学三角：{len(math_trig_questions)} 道")
        print(f"  数学数列：{len(math_seq_questions)} 道")
        print(f"  英语时态：{len(eng_tense_questions)} 道")
        print(f"  英语虚拟：{len(eng_subjunctive_questions)} 道")
        print(f"  英语从句：{len(eng_clause_questions)} 道")
        print(f"  物理牛顿：{len(phy_newton_questions)} 道")
        print(f"  物理电磁：{len(phy_em_questions)} 道")
        print(f"  化学氧化：{len(chem_redox_questions)} 道")
        print(f"  化学平衡：{len(chem_balance_questions)} 道")
        print("=" * 50)
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()