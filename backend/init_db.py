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
            # 数学知识点
            KnowledgePoint(name="集合", category_id=1, description="集合的基本概念和运算"),
            KnowledgePoint(name="函数", category_id=1, description="函数的性质和图像"),
            KnowledgePoint(name="三角函数", category_id=1, description="三角函数的定义和性质"),
            KnowledgePoint(name="数列", category_id=1, description="等差数列和等比数列"),
            KnowledgePoint(name="立体几何", category_id=1, description="空间几何体的性质"),
            
            # 英语知识点
            KnowledgePoint(name="时态", category_id=2, description="英语时态的用法"),
            KnowledgePoint(name="虚拟语气", category_id=2, description="虚拟语气的三种情况"),
            KnowledgePoint(name="定语从句", category_id=2, description="定语从句的引导词和用法"),
            KnowledgePoint(name="非谓语动词", category_id=2, description="不定式、动名词、分词的用法"),
            
            # 物理知识点
            KnowledgePoint(name="牛顿定律", category_id=3, description="牛顿三大定律"),
            KnowledgePoint(name="电磁感应", category_id=3, description="电磁感应现象"),
            KnowledgePoint(name="动量守恒", category_id=3, description="动量守恒定律"),
            
            # 化学知识点
            KnowledgePoint(name="化学平衡", category_id=4, description="化学平衡原理"),
            KnowledgePoint(name="氧化还原", category_id=4, description="氧化还原反应"),
            KnowledgePoint(name="有机化学", category_id=4, description="有机化合物的性质")
        ]
        db.add_all(knowledge_points)
        db.commit()
        
        # 创建题目
        questions = [
            # 数学题目
            Question(
                content="已知集合A={1,2,3}，B={2,3,4}，则A∩B=",
                question_type="single",
                difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "{1,2,3,4}"},
                    {"label": "B", "content": "{2,3}"},
                    {"label": "C", "content": "{1,4}"},
                    {"label": "D", "content": "∅"}
                ]),
                answer="B",
                explanation="交集是两个集合共有的元素组成的集合，A和B共有的元素是2和3。",
                category_id=1,
                knowledge_point_id=1
            ),
            Question(
                content="函数f(x)=x²-2x+1的最小值为",
                question_type="single",
                difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "-1"},
                    {"label": "B", "content": "0"},
                    {"label": "C", "content": "1"},
                    {"label": "D", "content": "2"}
                ]),
                answer="B",
                explanation="f(x)=(x-1)²≥0，当x=1时取最小值0。",
                category_id=1,
                knowledge_point_id=2
            ),
            Question(
                content="sin30°的值为",
                question_type="single",
                difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "1/2"},
                    {"label": "B", "content": "√2/2"},
                    {"label": "C", "content": "√3/2"},
                    {"label": "D", "content": "1"}
                ]),
                answer="A",
                explanation="sin30°=1/2，这是特殊角的三角函数值。",
                category_id=1,
                knowledge_point_id=3
            ),
            Question(
                content="等差数列{an}中，a1=1，d=2，则a10=",
                question_type="single",
                difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "17"},
                    {"label": "B", "content": "19"},
                    {"label": "C", "content": "21"},
                    {"label": "D", "content": "23"}
                ]),
                answer="B",
                explanation="等差数列通项公式：an=a1+(n-1)d，所以a10=1+(10-1)×2=19。",
                category_id=1,
                knowledge_point_id=4
            ),
            
            # 英语题目
            Question(
                content="I ___ to school by bus every day.",
                question_type="single",
                difficulty="easy",
                options=json.dumps([
                    {"label": "A", "content": "go"},
                    {"label": "B", "content": "goes"},
                    {"label": "C", "content": "going"},
                    {"label": "D", "content": "went"}
                ]),
                answer="A",
                explanation="every day表示经常性动作，用一般现在时。主语是I，动词用原形go。",
                category_id=2,
                knowledge_point_id=6
            ),
            Question(
                content="If I ___ you, I would study harder.",
                question_type="single",
                difficulty="hard",
                options=json.dumps([
                    {"label": "A", "content": "am"},
                    {"label": "B", "content": "was"},
                    {"label": "C", "content": "were"},
                    {"label": "D", "content": "be"}
                ]),
                answer="C",
                explanation="虚拟语气中，be动词统一用were。",
                category_id=2,
                knowledge_point_id=7
            ),
            Question(
                content="The book ___ by him last year is very popular.",
                question_type="single",
                difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "wrote"},
                    {"label": "B", "content": "writing"},
                    {"label": "C", "content": "written"},
                    {"label": "D", "content": "was written"}
                ]),
                answer="C",
                explanation="过去分词作定语，表示被动和完成。",
                category_id=2,
                knowledge_point_id=9
            ),
            
            # 物理题目
            Question(
                content="力是改变物体运动状态的原因",
                question_type="judge",
                difficulty="easy",
                options=None,
                answer="正确",
                explanation="根据牛顿第一定律，力是改变物体运动状态的原因，而不是维持物体运动的原因。",
                category_id=3,
                knowledge_point_id=10
            ),
            Question(
                content="下列关于电磁感应的说法正确的是",
                question_type="single",
                difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "感应电流的磁场总是阻碍原磁场的变化"},
                    {"label": "B", "content": "感应电流的磁场总是与原磁场方向相反"},
                    {"label": "C", "content": "感应电流的磁场总是促进原磁场的变化"},
                    {"label": "D", "content": "感应电流的磁场方向与原磁场方向无关"}
                ]),
                answer="A",
                explanation="楞次定律：感应电流的磁场总是阻碍引起感应电流的磁通量的变化。",
                category_id=3,
                knowledge_point_id=11
            ),
            
            # 化学题目
            Question(
                content="下列反应属于氧化还原反应的是",
                question_type="single",
                difficulty="medium",
                options=json.dumps([
                    {"label": "A", "content": "CaO + H₂O = Ca(OH)₂"},
                    {"label": "B", "content": "2Na + 2H₂O = 2NaOH + H₂↑"},
                    {"label": "C", "content": "CaCO₃ = CaO + CO₂↑"},
                    {"label": "D", "content": "NaOH + HCl = NaCl + H₂O"}
                ]),
                answer="B",
                explanation="氧化还原反应的特征是元素化合价发生变化。Na从0价变为+1价，H从+1价变为0价。",
                category_id=4,
                knowledge_point_id=14
            ),
            Question(
                content="化学平衡常数K只与温度有关",
                question_type="judge",
                difficulty="medium",
                options=None,
                answer="正确",
                explanation="化学平衡常数K只与温度有关，与浓度、压强等因素无关。",
                category_id=4,
                knowledge_point_id=13
            )
        ]
        db.add_all(questions)
        db.commit()
        
        print("数据库初始化成功！")
        print(f"创建了 {len(categories)} 个科目")
        print(f"创建了 {len(knowledge_points)} 个知识点")
        print(f"创建了 {len(questions)} 道题目")
        
    except Exception as e:
        print(f"初始化失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()