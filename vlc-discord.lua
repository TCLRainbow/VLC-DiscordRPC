local gameSDK = require 'lua-discordGameSDK'
local presence = {
  state = "", -- Second line
  details = "", -- Third line
  start_time = nil, -- Epoch
  end_time = nil,
  large_image = "", -- Image key
  large_text = "",
  small_image = "", -- Image key
  small_text = "",
  party_id = "",
  party_size = 0,
  party_max = 0,
  match_secret = "", -- Not exactly sure how to use them >.<
  join_secret = "",
  spectate_secret = ""
}

--[[ VLC extension]]--

function descriptor()
  return {
    title = "Discord Rich Presence",
    version = "1.0",
    author = "ChingDim",
    url = 'https://github.com/TCLRainbow/VLC-DiscordRPC',
    shortdesc = "Discord RPC",
    description = "Enables Discord RPC support for VLC",
    capabilities = {"menu", "input-listener"}
  }
end

function activate()

end

function input_changed()
  local rpc = gameSDK.initialize(757258842328399944)
  local d = vlc.dialog("Input changed!")
  local i = vlc.input.item()  -- input is renamed to player for VLC 4.0. See https://github.com/verghost/vlc-lua-docs
  local meta = i:metas()
  d:add_label(meta["filename"])
  d:show()
  --presence['state'] = "SAM IS 20 BRUH SO OLD"
  --rpc = gameSDK.updatePresence(rpc, presence)
end

function meta_changed()
end

function deactivate()
end