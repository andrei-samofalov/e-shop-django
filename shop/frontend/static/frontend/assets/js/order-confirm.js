var mix = {
    methods: {
        confirmOrder() {
            if (this.order) {
                this.postData('/api/orders/' + this.order.orderId + '/', {
                    ...this.order
                })
                    .then(this.basket = {})
                    .then(() => {
                        alert('Заказ подтвержден')
                        if (this.order.paymentType === 'someone') {
                            location.replace('/payment-someone/');
                        } else {
                            location.replace('/payment/')
                        }
                    })
                    .catch(() => {
                        console.warn('Ошибка при подтверждения заказа')
                    })
            }
        }
    },
    mounted() {
    },
    data() {
        return {}
    },
}