import router from './router'
import store from './store'
import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar
import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false }) // NProgress Configuration


// 在每个路由执行前执行的代码
router.beforeEach(async(to, from, next) => {
  console.log('permission.router.beforeeach')

  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  const hasToken = getToken()
  console.log('hasToken:' + hasToken)

  if (to.hidden) {
    if (hasToken) {
      if (to.path === '/login') {
        // TODO 如果用户已经登录，请求login页时，给他重定向到用户中心首页
        next()
        NProgress.done()
      } else {
        const hasGetUserInfo = store.getters.nick
        if (hasGetUserInfo) {
          next()
        } else {
          try {
            // get user info
            console.log('excute user/getInfo')
            await store.dispatch('user/getInfo')

            next()
          } catch (error) {
            // remove token and go to login page to re-login
            await store.dispatch('user/resetToken')
            Message.error(error || 'Has Error')
            next(`/login?redirect=${to.path}`)
            NProgress.done()
          }
        }
      }
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  } else {
    // 如果请求的是公开页面，那么就直接显示
    next()
    NProgress.done()
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
