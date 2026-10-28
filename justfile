# Requires you to have a .env.local.
# If you don't have one yet, copy it from `.env.local.template` and edit it to your liking.

set dotenv-filename := ".env.local"
set dotenv-required
set ignore-comments
set quiet
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

archipelago_root := absolute_path(env("ARCHIPELAGO_ROOT"))
archipelago := justfile_directory() / "external/archipelago"

python := absolute_path(env("PYTHON"))
seed := env("SEED")
temp_ap_dir := justfile_directory() / ".ap"

export SKIP_REQUIREMENTS_UPDATE := "1"
export AP_TEST_WORLDS := "gstla"  # 0.6.8 only

build_dir := justfile_directory() / "build"


[unix]
setup:
    mkdir -p "{{justfile_directory()}}/external"
    ln -sfn "{{archipelago_root}}" "{{archipelago}}"
    ln -sfn "{{justfile_directory()}}/worlds/gstla" "{{archipelago}}/worlds/gstla"

[windows]
setup:
    New-Item -ItemType Directory -Force "{{justfile_directory()}}/external" | Out-Null
    if (Test-Path -LiteralPath "{{archipelago}}") { (Get-Item -LiteralPath "{{archipelago}}").Delete() }
    New-Item -ItemType Junction -Path "{{archipelago}}" -Target "{{archipelago_root}}" | Out-Null
    if (Test-Path -LiteralPath "{{archipelago}}/worlds/gstla") { (Get-Item -LiteralPath "{{archipelago}}/worlds/gstla").Delete() }
    New-Item -ItemType Junction -Path "{{archipelago}}/worlds/gstla" -Target "{{justfile_directory()}}/worlds/gstla" | Out-Null


[working-directory: 'external/archipelago']
test *args: setup
    {{python}} -m pytest worlds/gstla/test {{args}}


# Requires AP 0.6.8+ to respect AP_TEST_WORLDS.
# You can still run it with 0.6.7, but it'll take ~20 mins instead of 2.
[working-directory: 'external/archipelago']
test-general *args: setup
    {{python}} -m pytest test/general -m world {{args}}


lint: setup
    uv run ruff check worlds

check-format: setup
    uv run ruff format --check worlds

check-types: setup
    uv run pyrefly check

check: lint check-format check-types


# Somewhat requires AP 0.6.8+. 0.6.7 has no --skip_open_folder and theoretically opens a file browser instead :|
# Also logs a few warnings/errors for other APWorlds. Can't turn off that they are even loaded. It is how it is.
[unix]
[working-directory: 'external/archipelago']
build: setup
    {{python}} Launcher.py "Build APWorlds" -- "Golden Sun The Lost Age" --skip_open_folder
    mkdir -p "{{build_dir}}"
    cp build/apworlds/gstla.apworld "{{build_dir}}/"
    echo "Built {{build_dir}}/gstla.apworld"

[windows]
[working-directory: 'external/archipelago']
build: setup
    {{python}} Launcher.py "Build APWorlds" -- "Golden Sun The Lost Age" --skip_open_folder
    New-Item -ItemType Directory -Force "{{build_dir}}" | Out-Null
    Copy-Item build/apworlds/gstla.apworld "{{build_dir}}/"
    Write-Output "Built {{build_dir}}/gstla.apworld"


# Server/Client Testing
local_server_port := env("LOCAL_SERVER_PORT")
out_dir := temp_ap_dir / "out"


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


[unix]
[working-directory: 'external/archipelago']
start-server: setup _prepare-ap-dir
    {{python}} Generate.py --seed {{seed}} --player_files_path "{{temp_ap_dir}}/players" --outputpath "{{out_dir}}"
    {{python}} MultiServer.py --port {{local_server_port}} --disable_save "{{out_dir}}"/AP_*.zip

[windows]
[working-directory: 'external/archipelago']
start-server: setup _prepare-ap-dir
    {{python}} Generate.py --seed {{seed}} --player_files_path "{{temp_ap_dir}}/players" --outputpath "{{out_dir}}"
    {{python}} MultiServer.py --port {{local_server_port}} --disable_save (Get-Item "{{out_dir}}/AP_*.zip").FullName


[working-directory: 'external/archipelago']
start-client *args: setup
    @echo "Load connector_bizhawk_generic.lua in the BizHawk Lua Console"
    {{python}} BizHawkClient.py --connect localhost:{{local_server_port}} {{args}}
