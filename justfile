# Requires you to have a .env.local.
# If you don't have one yet, copy it from .env.local.template and edit it to your liking.

set dotenv-filename := ".env.local"
set ignore-comments
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

archipelago_root := env("ARCHIPELAGO_ROOT", justfile_directory() / "../../archipelago")
archipelago := justfile_directory() / "external/archipelago"

# TODO: Also make python interpreter configurable (also see pyrefly config in pyproject.toml)
python := if os_family() == "windows" { archipelago / ".venv/Scripts/python.exe" } else { archipelago / ".venv/bin/python" }
seed := env("SEED", "1")
temp_ap_dir := justfile_directory() / ".ap"

# used by AP directly, not us
export SKIP_REQUIREMENTS_UPDATE := "1"
export AP_TEST_WORLDS := "gstla"


[unix]
setup:
    mkdir -p "{{justfile_directory()}}/external"
    ln -sfn "$(realpath "{{archipelago_root}}")" "{{archipelago}}"
    ln -sfn "{{justfile_directory()}}/worlds/gstla" "{{archipelago}}/worlds/gstla"

[windows]
setup:
    New-Item -ItemType Directory -Force "{{justfile_directory()}}/external" | Out-Null
    New-Item -ItemType Junction -Force -Path "{{archipelago}}" -Target (Resolve-Path "{{archipelago_root}}").Path | Out-Null
    New-Item -ItemType Junction -Force -Path "{{archipelago}}/worlds/gstla" -Target "{{justfile_directory()}}/worlds/gstla" | Out-Null


[working-directory: 'external/archipelago']
test *args: setup
    {{python}} -m pytest worlds/gstla/test {{args}}


check: setup
    uv run ruff check worlds
    uv run ruff format --check worlds
    uv run pyrefly check


# Server/Client Testing
local_server_port := env("LOCAL_SERVER_PORT", "38281")
bizhawk_dir := justfile_directory() / "../../tools/bizhawk"
emuhawk := env("EMUHAWK", if os_family() == "windows" { bizhawk_dir / "EmuHawk.exe" } else { bizhawk_dir / "EmuHawkMono.sh" })
out_dir := temp_ap_dir / "out"
out_base := out_dir / ("AP_" + seed)
multiworld_zip := out_base + ".zip"
patch_file := out_base + "_P1_Player.apgstla"
vanilla_rom := env("GSTLA_VANILLA_ROM", "")

# EmuHawk gets passed these two paths as they are. Breaks on WSL. TODO: WSL stuff
connector_lua := env("CONNECTOR_LUA", archipelago / "data/lua/connector_bizhawk_generic.lua")
patched_rom := env("GSTLA_PATCHED_ROM", out_base + "_P1_Player.gba")


[unix]
_prepare-ap-dir:
    rm -rf "{{temp_ap_dir}}"
    mkdir -p "{{temp_ap_dir}}/players" "{{out_dir}}"
    cp "{{justfile_directory()}}/fixtures/gstla-test.yaml" "{{temp_ap_dir}}/players/"

[windows]
_prepare-ap-dir:
    Remove-Item -Recurse -Force -ErrorAction Ignore "{{temp_ap_dir}}"
    New-Item -ItemType Directory -Force "{{temp_ap_dir}}/players", "{{out_dir}}" | Out-Null
    Copy-Item "{{justfile_directory()}}/fixtures/gstla-test.yaml" "{{temp_ap_dir}}/players/"


[working-directory: 'external/archipelago']
start-server: setup _prepare-ap-dir
    {{python}} Generate.py --seed {{seed}} --player_files_path "{{temp_ap_dir}}/players" --outputpath "{{out_dir}}"
    {{python}} MultiServer.py --port {{local_server_port}} --disable_save "{{multiworld_zip}}"


[working-directory: 'external/archipelago']
patch: setup
    {{python}} -m zipfile -e "{{multiworld_zip}}" "{{out_dir}}"
    {{python}} -c "import settings, Patch; s = settings.get_settings(); s.gstla_options.rom_file = r'{{vanilla_rom}}' or s.gstla_options.rom_file; print(Patch.create_rom_file(r'{{patch_file}}'))"


[working-directory: 'external/archipelago']
start-client *args: setup
    @echo "Load connector_bizhawk_generic.lua in the BizHawk Lua Console"
    {{python}} BizHawkClient.py --connect localhost:{{local_server_port}} {{args}}


start-game: setup
    "{{emuhawk}}" "--lua={{connector_lua}}" "{{patched_rom}}"
