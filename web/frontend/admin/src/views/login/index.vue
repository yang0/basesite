<template>
  <div class="login-container">
    <ApolloMutation
      :mutation="require('@/graphql/userLogin.gql')"
      :variables="{tel, password}"
      class="wrapper"
      @done="onDone"
    >
      <el-form
        slot-scope="{ mutate, loading, gqlError: error }"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        auto-complete="on"
        label-position="left"
      >
        <div class="title-container">
          <h3 class="title">登 录</h3>
        </div>

        <el-form-item prop="tel">
          <span class="svg-container">
            <svg-icon icon-class="user"/>
          </span>
          <el-input
            ref="tel"
            v-model="loginForm.tel"
            placeholder="手机号码"
            name="tel"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>

        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password"/>
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="mutate"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"/>
          </span>
        </el-form-item>

        <el-button
          :loading="loading"
          type="primary"
          style="width:100%;margin-bottom:30px;"
          @click.native.prevent="mutate"
        >Login</el-button>

        <div class="tips">
          <span style="margin-right:20px;">username: admin</span>
          <span>password: any</span>
        </div>
      </el-form>
    </ApolloMutation>
  </div>
</template>

<script>
import USER_CURRENT from '@/graphql/userCurrent.gql'
import { onLogin } from '@/vue-apollo'


export default {
  name: "Login",
  data() {
    const validateTel = (rule, value, callback) => {
      this.tel = value
      if (value.length != 11) {
        callback(new Error("请输入正确的手机号"));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      this.password = value
      if (value.length < 6) {
        callback(new Error("请输入正确的密码"));
      } else {
        callback();
      }
    };
    return {
      loginForm: {
        tel: "",
        password: ""
      },
      tel: "",
      password: "",
      loginRules: {
        tel: [
          { required: true, trigger: "blur", validator: validateTel }
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ]
      },
      loading: false,
      passwordType: "password",
      redirect: undefined
    };
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect;
      },
      immediate: true
    }
  },
  methods: {
     async onDone (result) {
      // 如果没有拿到token就直接返回
      if (!result.data.userLogin) return

      const apolloClient = this.$apollo.provider.defaultClient
      // Update token and reset cache
      const token = result.data.userLogin.token
      await onLogin(apolloClient, token)

      //
      this.$store.dispatch('user/onLogin', token)

      // Update cache
      apolloClient.writeQuery({
        query: USER_CURRENT,
        data: {
          userCurrent: result.data.userLogin.user,
        },
      })  

      

      this.$router.push({ path: this.redirect || "/" });
      this.loading = false
      console.log("aa")
    },

    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
      this.$nextTick(() => {
        this.$refs.password.focus();
      });
    },
    
  },
};
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
