- udp send discovery
- udp recv discovery
- udp send discovery_reply to discovery
- add player to player list during discovery and discovery_reply
- display players in LobbyScene

- send tcp game_request to player from LobbyScene
- send tcp game_reply (+/-) to game_request
- "go back" to lobby on -game_reply
- start game on +game_reply
- show popup on recv game_request

- send tcp game_move on every move done