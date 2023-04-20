var mix = {
    methods: {
        getBanners() {
            this.getData("/api/banners/")
              .then(data => {
                this.banners = data
              }).catch(() => {
                  this.banners = []
                  console.warn('Ошибка при получении баннеров')
              })
        },
        getPopularProducts() {
            this.getData("/api/products/popular/")
              .then(data => {
                this.popularCards = data
              }).catch(() => {
                  this.popularCards = []
                  console.warn('Ошибка при получении списка популярных товаров')
            })
        },
        getLimitedProducts() {
            this.getData("/api/products/limited/")
              .then(data => {
                this.limitedCards = data
              }).catch(() => {
                  this.limitedCards = []
                  console.warn('Ошибка при получении списка лимитированных товаров')
            })
        },
    },
    mounted() {
        this.getBanners();
        this.getPopularProducts();
        this.getLimitedProducts();
    },
//    created() {
//      this.getLimitedProducts()
//    },
    data() {
        return {
            banners: [],
            popularCards: [],
            limitedCards: [],
        }
    }
}