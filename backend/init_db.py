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
        
        categories = [
            Category(name="数学", description="数学学科"),
            Category(name="英语", description="英语学科"),
            Category(name="物理", description="物理学科"),
            Category(name="化学", description="化学学科")
        ]
        db.add_all(categories)
        db.commit()
        
        knowledge_points = [
            KnowledgePoint(name="集合", category_id=1, description="集合的基本概念和运算"),
            KnowledgePoint(name="函数", category_id=1, description="函数的性质和图像"),
            KnowledgePoint(name="三角函数", category_id=1, description="三角函数的定义和性质"),
            KnowledgePoint(name="时态", category_id=2, description="英语时态的用法"),
            KnowledgePoint(name="虚拟语气", category_id=2, description="虚拟语气的三种情况"),
            KnowledgePoint(name="牛顿定律", category_id=3, description="牛顿三大定律"),
            KnowledgePoint(name="电磁感应", category_id=3, description="电磁感应现象"),
            KnowledgePoint(name="化学平衡", category_id=4, description="化学平衡原理")
        ]
        db.add_all(knowledge_points)
        db.commit()
        
        questions = [
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
                knowledge_point_id=4
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
                knowledge_point_id=5
            ),
            Question(
                content="力是改变物体运动状态的原因",
                question_type="judge",
                difficulty="easy",
                options=None,
                answer="正确",
                explanation="根据牛顿第一定律，力是改变物体运动状态的原因，而不是维持物体运动的原因。",
                category_id=3,
                knowledge_point_id=6
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