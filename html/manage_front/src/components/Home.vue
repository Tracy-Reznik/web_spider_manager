<template>
    <div class="homeWrap">
    <el-container class="main_container">
        <el-header style="background: #409eff;color: #fff;height: 60px;padding: 0px">
            <el-menu
                     mode="horizontal"
                     background-color="#409eff"
                     text-color="#fff"
                     active-text-color="#fff"
                     menu-trigger="click"
                     >
                <el-menu-item index="0" style="font-size: 25px" mode="horizontal" route="/">{{title}}</el-menu-item>
                <div class="flex-grow" />
                <el-menu-item index="1">{{username}}</el-menu-item>
            </el-menu>

        </el-header>
        <el-container>
            <el-aside width="250px" style="background: #343a40">Aside</el-aside>
            <el-main><router-view name="main-view"></router-view></el-main>
        </el-container>
    </el-container>
    </div>
</template>


<script>
export default {
    name: "Home",
    data() {
        return {
            title: document.title,
            username:"user"
        }
    },
    computed:{
        getImg(){
            return document.server+"api/img/"+this.username;
        }
    },
    methods:{

    }
}
</script>

<style scoped>
.homeWrap {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
.main_container {
    height: 100%;
}

.flex-grow {
    flex-grow: 1;
}

</style>