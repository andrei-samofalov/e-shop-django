var mix = {
    methods: {
        getUserAccount() {
            this.getData("/api/account/").then(data => {
                this.firstname = data.firstname
                this.secondname = data.secondname
                this.surname = data.surname
                this.avatar = data.avatar
                this.orders = data.orders
            })
        },
    },
    mounted() {
        this.getUserAccount();
    },
    data() {
        return {
            firstname: "",
            secondname: "",
            surname: "",
            avatar: {},
            orders: [],
        }
    },
    computed: {
        fullName() {
            return [this.surname, this.firstname, this.secondname].join(" ")
        },
    },
}