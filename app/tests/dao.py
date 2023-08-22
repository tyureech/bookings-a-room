from app.dao.base import BaseDAO
from app.tests.models import TestModel

class TestBaseDAO(BaseDAO):
    model = TestModel
