var mix = {
    // может это сделать через шаблонизатор?
    computed: {
        tags() {
            return this.topTags.filter(tag => this.product?.tags?.includes(tag.name))
        }
    },
    methods: {
        changeCount(value) {
            this.count = this.count + value
            if (this.count < 1) this.count = 1
        },
        getProduct() {
            this.getData(`/api/products/` + pk + `/`).then(data => {
                this.product = {
                    ...this.product,
                    ...data
                }
            }).catch(() => {
                this.product = {}
                console.warn('Ошибка при получении товара')
            })
        },
        submitReview() {
            this.postData('/api/products/' + this.product.id + '/review/', {
                    author: this.review.author,
                    email: this.review.email,
                    text: this.review.text,
                    rate: this.review.rate
                }
            ).then(data => {
                this.product.reviews = data
                alert('Отзыв опубликован')
                this.review.author = ''
                this.review.email = ''
                this.review.text = ''
                this.review.rate = 5
            }).catch(() => {
                console.warn('Ошибка при публикации отзыва')
            })
        }
    },
    mounted() {
        this.getProduct();
    },
    data() {
        return {
            product: {},
            count: 1,
            review: {
                author: '',
                email: '',
                text: '',
                rate: 5
            }
        }
    },
}