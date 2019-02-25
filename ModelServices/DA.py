from db import session_scope

class DataBaseAccess:
    def data_select(self, models, inner_join_list=[], outer_join_list=[], filter_list=None):

        self.filter_list = filter_list
        with session_scope() as session:
            # 필요한 모델들로 select문을 생성한다.
            self.query = session.query(*models)

            # join문을 추가한다.
            for join in inner_join_list:
                self.query.join(*join)

            # outerjoin문을 추가한다.
            for join in outer_join_list:
                self.query.outerjoin(*join)

            # 필터 필요시 필터를 수행한다.
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
                # 모델, 컬럼명, 조건, 대상 값
                model, key, op, value = raw
            except ValueError:
                raise Exception('필터 형식 또는 데이터가 맞지 않습니다 : %s' % raw)

            # 모델 클래스의 필드(컬럼)를 가져온다.
            column = getattr(model, key, None)
            if not column:
                raise Exception("모델에 %s 필드가 없습니다." % key)

            # 조건이 in이라면 아래 작업을 수행한다.
            if op == 'in':
                if isinstance(value, list):
                    filt = self.query.in_(value)
                else:
                    filt = self.query.in_(value.split(','))
            # 그 외 조건은 아래 작업을 수행한다.
            else:
                try:
                    # 컬럼에 따라 조건 변수가 어려개 존재한다.
                    # 모두 대응하기 위해 아래 와 같이 체크하고 설정
                    attr = list(filter(lambda e: hasattr(column, e % op), ['%s', '%s_', '__%s__']))[0] % op
                except IndexError:
                    raise Exception('해당 컬럼에는 {} 없는 비교연산 입니다 : {}'.format(column, op))

                if value == 'null':
                    value = None
                # 조건을 설정한다.
                filt = getattr(column, attr)(value)

            # 필터 쿼리를 추가한다.
            self.query = self.query.filter(filt)
