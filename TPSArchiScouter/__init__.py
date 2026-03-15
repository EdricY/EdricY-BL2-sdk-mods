import os
import unrealsdk
import unrealsdk.unreal as unreal
from mods_base import build_mod, hook, SliderOption, ENGINE
# from save_options.options import HiddenSaveOption


mod_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(mod_dir) # sdk_mods/ if running unzipped
if parent_dir.endswith(".sdkmod") or parent_dir.endswith(".zip"):
    parent_dir = os.path.dirname(parent_dir)
storage_dir = os.path.join(parent_dir, "ArchiLogs")
os.makedirs(storage_dir, exist_ok=True)

log_filepath = os.path.join(storage_dir, "log.txt")

@hook("WillowGame.WillowPlayerPawn:DoSprint")
def sprint_pressed(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    self.SprintingPct = sprint_option.value * .1

@hook("WillowGame.WillowAIPawn:Died")
def on_killed_enemy(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    print(self.AIClass.Name)
    print(self.GetTransformedName())
    enemy_key = self.AIClass.Name
    log_to_file(f"killed: {enemy_key}")

@hook("WillowGame.Behavior_DiscoverLevelChallengeObject:ApplyBehaviorToContext")
def discover_level_challenge_object(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    pathname = caller.ContextObject.PathName(caller.ContextObject)
    log_to_file(f"maybe symbol: {pathname}")

def get_current_map():
    if ENGINE and ENGINE.GetCurrentWorldInfo:
        wi = ENGINE.GetCurrentWorldInfo()
        if wi and wi.GetMapName:
            return str(wi.GetMapName()).casefold()
    return "none"

current_map = None
@hook("WillowGame.WillowPlayerController:ClientSetPawnLocation")
def moved_map(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    new_map_area = get_current_map()
    if current_map != new_map_area:
        current_map = new_map_area
        log_to_file(f"moved to region: {current_map}")

def get_pos_str(obj):
    # old way: f"{str(wvm.Outer)}~{str(wvm.Location.X)},{str(wvm.Location.Y)}"
    map_area = get_current_map()
    return f"{map_area}~{int(obj.Location.X)},{int(obj.Location.Y)}"


@hook("WillowGame.WillowInteractiveObject:UseObject")
def use_vending_machine(self, caller: unreal.UObject, function: unreal.UFunction, params: unreal.WrappedStruct):
    pos_str = get_pos_str(self)
    if self.Class and self.Class.Name == "WillowVendingMachine":
        log_to_file(f"vending machine: {pos_str}")
        return
    else:
        log_to_file(f"interacted with: {pos_str}")

def log_to_file(line):
    print(line)
    if not log_filepath:
        print("don't know where to log")
        with open(os.path.join(storage_dir, "unknown.log.txt"), 'a') as f:
            f.write(line + "\n")
        return
    with open(log_filepath, 'a') as f:
        f.write(line + "\n")


sprint_option = SliderOption(
    identifier="Sprint Speed",
    value=15,
    min_value=5,
    max_value=50,
    description=(
        "Sprint Speed"
    ),
)

mod_instance = build_mod(
    options=[sprint_option],
    hooks=[
        sprint_pressed,
        on_killed_enemy,
        discover_level_challenge_object,
        use_vending_machine,
    ]
)
