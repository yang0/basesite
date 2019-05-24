import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'
import { apolloProvider } from '@/main'

// export function request(gqlFile, variables){
//   console.log("utils.request")
//   apolloClient.query({
//     query: gqlFile,
//     variables: variables
//   })
// }


export const request = (searchR, params) => apolloProvider.apolloClient.query({
  query: searchR,
  variables: params
})








