// import request from '@/utils/request'
import USER_CURRENT from '@/graphql/userCurrent.gql'
import { apolloProvider } from '@/main'

// export function login(data) {
//   return request({
//     url: '/user/login',
//     method: 'post',
//     data
//   })
// }

export function getInfo(token) {
  console.log("user.getInfo")
  apolloProvider.apolloClient.query({
    query: USER_CURRENT
  })
}

// export function logout() {
//   return request({
//     url: '/user/logout',
//     method: 'post'
//   })
// }
