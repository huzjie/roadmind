"""流水线测试。"""
def test_driving_pipeline(mock_engine):
    from roadmind.config.loader import load_config
    from roadmind.pipeline import DrivingPipeline
    pipeline = DrivingPipeline(load_config(), mock_engine)
    result = pipeline.run(None)
    assert result["plan"]["command"].action in ("KEEP_LANE", "STOP", "SLOW_DOWN")
    summary = pipeline.summarize(result)
    assert "指令" in summary
