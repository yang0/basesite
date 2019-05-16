const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  token: state => state.user.token,
  tel: state => state.user.tel,
  nick: state => state.user.nick,
  avatar: state => state.user.avatar,
  name: state => state.user.nick
}
export default getters
