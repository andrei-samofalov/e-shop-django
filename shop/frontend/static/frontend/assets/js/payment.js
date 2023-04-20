var mix = {
    methods: {
        submitPayment() {
            this.postData('/api/payment/', {
                name: this.name,
                number: this.number,
                year: this.year,
                month: this.month,
                code: this.code,
            }).then(() => {
                alert('Оплата прошла успешно')
                this.number = ''
                this.name = ''
                this.year = ''
                this.month = ''
                this.code = ''

                this.basket = {}
                location.replace('/')

            }).catch(() => {
                console.warn('Ошибка при оплате')
                alert('Ошибка при оплате, введите другую карту для оплаты')
            })
        },
        sleep() {
            function sleep(ms) {
                return new Promise(resolve => setTimeout(resolve, ms));
            }
        }
    },
    data() {
        return {
            number: '',
            month: '',
            year: '',
            name: '',
            code: ''
        }
    }
}