import pytest

from app.tests.dao import TestBaseDAO


@pytest.mark.parametrize("id, res", [(1, 1), (2, 2), (100, None)])
async def test_base_get_by_id(id: int, res: int | None):
    data = await TestBaseDAO.get_by_id(id=id)
    if data:
        assert data.id == res
    else:
        assert data == res


@pytest.mark.parametrize("name, res", [
        ("Test1", "Test1"), 
        ("Test2", "Test2"), 
        ("...", None),
    ]
)
async def test_base_get_one_or_none(name: str, res: str | None):
    data = await TestBaseDAO.get_one_or_none(name=name)
    if data:
        assert data.name == res
    else:
        assert data == res


@pytest.mark.parametrize("filter, is_present", [
        ({"name": "Test1"}, True),
        ({"image_id": 1}, True),
        ({}, True),
        ({"image_id": 10}, False),
    ]
)
async def test_base_find_all(filter: dict, is_present: bool):
    data = await TestBaseDAO.find_all(**filter)
    assert (len(data) > 0) is is_present
