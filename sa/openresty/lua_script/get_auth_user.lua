-- 解析jwt token，获取用户的id，结合post及get数据，记录在日志中。
local cjson = require "cjson"
local jwt = require "resty.jwt"

local M = {}

function M.auth(secretKey)
    -- require Authorization request header
    local auth_header = ngx.var.http_Authorization

    if auth_header == nil then
        return
    end

    -- require Bearer token
    local _, _, token = string.find(auth_header, "Bearer%s+(.+)")

    if token == nil then
        return
    end

    local jwt_obj = jwt:verify(secretKey, token)
    if jwt_obj.verified == false then
        ngx.log(ngx.WARN, "Invalid token: ".. jwt_obj.reason)
        return
    end

    -- ngx.log(ngx.INFO, "JWT: " .. cjson.encode(jwt_obj))

    -- write the uid variable
    -- ngx.var.uid = jwt_obj.payload.tel

    return jwt_obj.payload

    -- ngx.say(userKeyName, ":", userKeyValue)
end

-- 获取token中关键的用户信息
function M.getUserInfo(secretKey)
    local payload = M.auth(secretKey)
    if payload == nil then
        return "anonymouse"
    end

    local userInfo = {}
    

    for key, var in pairs(payload) do
        if key ~= "origIat" and key ~= "exp" then
            -- 对键值对进行拼接，形成字符串的格式： key1=var1;key2=var2
            table.insert(userInfo, key)
            table.insert(userInfo, "=")
            table.insert(userInfo, var)
            table.insert(userInfo, ";")
        end
    end

    return table.concat(userInfo)
end




return M