<template>
    <div >
        <Header></Header>
        <Banner></Banner>
        <Footer></Footer>

    </div>
</template>

<script>
import Banner from "./common/Banner";
import Footer from "./common/Footer";
import Header from "./common/Header";

export default {
    name: "Home",
    components:{
        Header:Header,
        Footer:Footer,
        Banner:Banner,

    }
}
</script>

<style scoped>

</style>
