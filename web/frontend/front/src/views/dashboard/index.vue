
<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
    <div>{{ hello }}</div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import USERS_ALL from '@/graphql/usersAll.gql'

export default {
  name: 'Dashboard',
  data() {
    return {
      // 初始化你的 apollo 数据
      hello: ''
    }
  },
  apollo: {
    hello: {
      query: USERS_ALL,
      variables() {
        return {
          tel: '001',
          nick: 'yang0'
        }
      },
      update: data => data
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
