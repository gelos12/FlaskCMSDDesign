#FlaskCMSDDesign.

`python -v 3.7.x`, `flask -v 1.0.2`, `SQLAlchemy -v 1.2.18`

`CMSD Design`은 Controller, Model, modelService, Database access의 약자이다.
flask를 활용하면서 DB접근시 어떻게 하면 효율적으로 할 수 있을까 고민하며 설계해보았다.


1. Controller
    - 컨트롤러는 사용자가 요청한 데이터를 제공하기 위해 필요한 비즈니스 로직과 결과값 전달을 담당한다.
    
    `MemoController.py`
    ```
    def memo_controller():
        memo_service = MemoService()
        if request.method == 'GET':
            memo = memo_service.get_memo().first()
            res = {
                'id': memo[0].memo_id,
                'author': memo[1].name,
                'title': memo[0].title,
                'content': memo[0].content
            }
        json_res = json.dumps(res)
        return jsonify(code="0", data=json_res)
    ``` 
        
2. Model
    - 데이터베이스 테이블과 1:1 매핑되는 파이썬 객체
    
    `MemoModel.py`
    ```
    class Memo(Base):
        __tablename__ = 'Memo'
    
        memo_id = Column(String(20), primary_key=True)
        user_id = Column(String(20))
        title = Column(String(20))
        content = Column(String(100))
    ```
    `UserModel.py`
    ```
    class User(Base):
        __tablename__ = 'User'
    
        user_id = Column(String(20), primary_key=True)
        name = Column(String(20))

    ```
3. modelService
    - 컨트롤러에서 요청한 특정 데이터를 가져오기 위한 정보들( 모델, 조인조건, 필터조건 )을 취합하고 데이터베이스 접근 객체에 요청한 후 결과를 컨트롤러에 리턴
    
    `MemoService.py`
    
    ```
    class MemoService:
        def __init__(self):
            self.da = DataBaseAccess()
    
        def get_memo(self):
            models = [Memo, User.name]
    
            inner_join_list = [
                (User, User.user_id == Memo.user_id)
            ]
    
            memo = self.da.data_select(models, inner_join_list=inner_join_list)
    
            return memo
    ```
    
4. Database access
    - 모델 서비스에서 취합해준 정보를 토대로 데이터베이스에 접근하여 얻은 결과를 모델 서비스에 전달해준다.
    
    `DAO.py`
    ```
    class DataBaseAccess:
        def data_select(self, models, inner_join_list=[], outer_join_list=[], filter_list=None):
    
            self.filter_list = filter_list
            with session_scope() as session:
                self.query = session.query(*models)
    
                for join in inner_join_list:
                    self.query.join(*join)
    
                for join in outer_join_list:
                    self.query.outerjoin(*join)
    
                if self.filter_list is not None:
                    self.__filter()
    
                return self.query
    
        def data_insert(self):
            pass
    
        def data_update(self):
            pass
    
        def data_delete(self):
            pass
    
        def __filter(self):
            for raw in self.filter_list:
                try:
                    model, key, op, value = raw
                except ValueError:
                    raise Exception('필터 형식 또는 데이터가 맞지 않습니다 : %s' % raw)
    
                column = getattr(model, key, None)
                if not column:
                    raise Exception("모델에 %s 필드가 없습니다." % key)
    
                if op == 'in':
                    if isinstance(value, list):
                        filt = self.query.in_(value)
                    else:
                        filt = self.query.in_(value.split(','))
                else:
                    try:
                        attr = list(filter(lambda e: hasattr(column, e % op), ['%s', '%s_', '__%s__']))[0] % op
                    except IndexError:
                        raise Exception('해당 컬럼에는 {} 없는 연산 입니다 : {}'.format(column, op))
    
                    if value == 'null':
                        value = None
                    filt = getattr(column, attr)(value)
    
                self.query = self.query.filter(filt)
    ```
##REFERENCE
 `filter method` [Ruddra's Blog](https://ruddra.com/posts/dynamically-constructing-filters-based-on-string-input-using-sqlalchemy/)
##LICENSED
MIT
