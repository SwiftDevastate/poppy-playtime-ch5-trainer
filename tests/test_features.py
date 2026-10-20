from trainer_core.features.base import TrainerFeature


class _StubFeature(TrainerFeature):
    name = "stub"

    def __init__(self):
        self.called = []

    def _apply(self):
        self.called.append("apply")

    def _revert(self):
        self.called.append("revert")


def test_toggle_cycle():
    f = _StubFeature()
    f.enable()
    f.enable()
    f.disable()
    assert f.called == ["apply", "revert"]
    assert f._enabled is False