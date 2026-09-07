"""VQA 测试。"""
def test_scene_qa(mock_engine):
    from roadmind.vqa.scene_qa import SceneQA
    qa = SceneQA(mock_engine)
    res = qa.ask("画面里有什么？")
    assert res.question == "画面里有什么？"
    assert res.answer
