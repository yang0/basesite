import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'
import { apolloProvider } from '@/main'
import gql from 'graphql-tag'
import USER_CURRENT from '@/graphql/userCurrent.gql'

const state = {
  token: getToken(),
  nick: '',
  tel: '',
  avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NICK: (state, nick) => {
    state.nick = nick
  },
  SET_TEL: (state, tel) => {
    state.tel = tel
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { data } = response
        commit('SET_TOKEN', data.token)
        setToken(data.token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 用户登录后保持token
  onLogin({ commit }, token) {
    commit('SET_TOKEN', token)
    setToken(token)
  },

  // get user info
  getInfo({ commit }, client) {
    return new Promise((resolve, reject) => {
      console.log("store.modules.user.getInfo.promise")
      console.log("apolloProvider.apolloClient:"+ apolloProvider.defaultClient)
      apolloProvider.defaultClient.query({query: USER_CURRENT}).then(response => {
        console.log(response)

        const { data } = response

        if (!data || !data.userCurrent) {
          reject('用户认证失败，请重新登录')
        }

        const { nick, tel } = data.userCurrent
        commit('SET_NICK', nick)
        commit('SET_TEL', tel)

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state }) {
    commit('SET_TOKEN', '')
    removeToken()
    resetRouter()
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      removeToken()
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

