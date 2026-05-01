from mods_base import build_mod, hook
from unrealsdk.hooks import Block
from unrealsdk.unreal import BoundFunction, UObject, WrappedStruct

@hook("Engine.WillowInventory:GetInventorySpaceRequirement")
def block_space_requirement(obj: UObject, args: WrappedStruct, ret, func: BoundFunction):
  return Block, 0

build_mod(
  hooks=[block_space_requirement],
)