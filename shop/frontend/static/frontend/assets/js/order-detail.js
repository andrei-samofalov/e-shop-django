var mix = {
    methods: {
        getOrder(id) {
            this.getData(`/api/orders/` + id + '/').then(data => {
                this.orderId = data.orderId
                this.createdAt = data.createdAt
                this.fullName = data.fullName
                this.phone = data.phone
                this.email = data.email
                this.deliveryType = data.deliveryType
                this.city = data.city
                this.address = data.address
                this.paymentType = data.paymentType
                this.status = data.status
                this.totalCost = data.totalCost
                this.products = data.products
                this.count = data.count
                if (typeof data.paymentError !== 'undefined') {
                    this.paymentError = data.paymentError
                }
            })
        },
    },
    mounted() {
        this.getOrder(pk);

    },
    data() {
        return {
            orderId: null,
            createdAt: '',
            fullName: '',
            phone: '',
            email: '',
            deliveryType: '',
            city: '',
            address: '',
            paymentType: '',
            status: '',
            totalCost: 0,
            products: '',
            count: 0,
            paymentError: null,
        }
    },
}