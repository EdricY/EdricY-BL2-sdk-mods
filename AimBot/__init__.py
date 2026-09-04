import unrealsdk.unreal as unreal
import unrealsdk
from mods_base import get_pc, build_mod, hook
from unrealsdk.hooks import Block, Type
from ui_utils import show_chat_message
import math as m

# from juso's uemath
PI = m.pi
URU_360 = 65536
URU_180 = 32768
URU_90 = URU_180 // 2  # 16384
URU_45 = URU_180 // 4  # 8192
URU_1 = URU_360 // 360  # ~182

URU_TO_RADIANS = PI / URU_180  # Multiply by this to convert from Uru to radians
RADIANS_TO_URU = (
  URU_180 / PI
)  # Multiply by this to convert from radians to Uru  value is
def vector_to_rotator(vector):
  """Convert a normalized Vector to a Rotator."""
  x, y, z = vector
  # print(x)
  pitch = m.atan2(z, m.sqrt(x * x + y * y)) * RADIANS_TO_URU
  yaw = m.atan2(y, x) * RADIANS_TO_URU
  roll = 0
  return int(pitch), int(yaw), roll

# TODO: fill this out
crit_spots = {
  # "BodyClass_Bruiser": "L_Thigh"
  "BodyClass_Bruiser": ["Head"],
  "BodyClass_BadassMidget": ["Gore_Head"],
  "BodyClass_LoaderGUN": ["L_Clav", "R_Clav", "Eye"],
  "BodyClass_LoaderEXP": ["L_Clav", "R_Clav", "Eye"],
  "BodyClass_LoaderWAR": ["L_Clav", "R_Clav", "Eye"],
  "BodyClass_LoaderJET": ["L_Clav", "R_Clav", "Eye"],
  "BodyClass_LoaderHOT": ["L_Clav", "R_Clav", "Eye"],
  "BodyClass_LoaderBUL": ["R_Clav", "Eye"],
  "BodyClass_LoaderBadass": ["L_Clav", "R_Clav", "Eye"],
}

def region_is_damaged(pawn, bone_name):
  # hrh = pawn.MyHitRegionHelper
  if bone_name == "L_Clav":
    data = pawn.GetInstanceData("Switch_ArmGone_L", ())
    if data[1][0].Int == 1:
      return True
  if bone_name == "R_Clav":
    data = pawn.GetInstanceData("Switch_ArmGone_R", ())
    if data[1][0].Int == 1:
      return True
  return False


def find_crit_attachment_name(body_class, pawn):
  if body_class.Name in crit_spots:
    crit_list = crit_spots[body_class.Name]
    i = 0
    while region_is_damaged(pawn, crit_list[i]) and i + 1 < len(crit_list):
      i += 1
    return crit_spots[body_class.Name][i]


  # unrecorded enemy, attempt to find...
  for a in body_class.BodyComposition.Attachments:
    hrd = a.Data.ComponentData.HitRegionDefinition
    if hrd and hrd.bCriticalHit:
      # return hrh.GetBoneNameFromHitComponent(hrd)
      # crit_spots[body_class] = a.Data.Name
      # return a.Data.Name
      # crit_spots[body_class] = a.Data.ComponentData.MeshSocketName
      return a.Data.ComponentData.MeshSocketName
  for hrd in body_class.HitRegionList:
    if hrd and hrd.bCriticalHit:
      # return hrh.GetBoneNameFromHitComponent(hrd)
      # crit_spots[body_class] = hrd.RegionBoneNames[0]
      return hrd.RegionBoneNames[0]

  return None


@hook("Engine.PlayerController:PlayerTick")
def tick(obj: unreal.UObject, args: unreal.WrappedStruct, ret, func: unreal.BoundFunction):
  pc = get_pc()
  pp = pc.Pawn
  if not pp:
    return
  weapon = pp.Weapon
  if not weapon:
    return

  target = pc.GetPawnAutoAimTarget()
  if target and weapon.ZoomState == 2: # EZoomState.ZST_Zoomed
    body_class = target.BodyClass
    att_name = find_crit_attachment_name(body_class, target)
    # print(body_class.Name)
    # print(att_name)
    loc = None
    if att_name:
      try:
        (_, loc, _) = target.GetWorldBodyAttachmentLocationAndRotation(att_name, unrealsdk.make_struct("Vector"), unrealsdk.make_struct("Rotator"))
      except:
        print("can't find " + att_name)
    if not loc:
      loc = target.Location

    px = pp.Location.X
    py = pp.Location.Y
    pz = pp.Location.Z + pp.EyeHeight
    vec = (loc.X - px, loc.Y - py, loc.Z - pz)
    
    rot = vector_to_rotator(vec)
    pc.Pawn.SetViewRotation(unrealsdk.make_struct("Rotator", Pitch=rot[0], yaw=rot[1], roll=rot[2]))
    pc.CurrentWanderAccuracy = 0

# for some debug info
@hook("WillowGame.WillowPlayerInput:DuckPressed")
def crouch(obj: unreal.UObject, args: unreal.WrappedStruct, ret, func: unreal.BoundFunction):
  print(crit_spots)
  target = get_pc().GetPawnAutoAimTarget()
  print(target)
  print(target.GetHitLocationBody())

mod_instance = build_mod(hooks=[
  tick,
  crouch,
])

