import unrealsdk.unreal as unreal
from mods_base import build_mod, get_pc, hook
from unrealsdk.hooks import Block, prevent_hooking_direct_calls

@hook("WillowGame.WillowPawn:SetGameStage")
def set_game_stage(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
  if self.Class.Name == "WillowPlayerPawn":
    return None

  level = get_pc().PlayerReplicationInfo.ExpLevel

  with prevent_hooking_direct_calls():
    params(level)

  return Block

build_mod(hooks=[set_game_stage])