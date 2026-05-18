"""Refresh helper for metrics + ui_state inside TouchDesigner."""
def refresh(owner=None):
    if owner is None:
        owner = parent()
    owner.op('metrics_engine').module.compute_and_store_touchdesigner(owner=owner)
    owner.op('ui_state').module.compute_and_store_touchdesigner_ui(owner=owner)
    return owner.fetch('ui_state', {})
