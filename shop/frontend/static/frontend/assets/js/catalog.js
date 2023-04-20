var mix = {
    methods: {
        setTag(id) {
            this.topTags = this.topTags.map(tag => {
                return tag.id === id
                    ? {
                        ...tag,
                        selected: !tag.selected
                    }
                    : tag
            })
            this.getCatalogs()
        },
        setSort(id) {
            if (this.selectedSort?.id === id) {
                this.selectedSort.selected =
                    this.selectedSort.selected === 'dec'
                        ? 'inc'
                        : 'dec'
            } else {
                if (this.selectedSort) {
                    this.selectedSort = null
                }
                this.selectedSort = this.sortRules.find(sort => sort.id === id)
                this.selectedSort = {
                    ...this.selectedSort,
                    selected: 'dec'
                }
            }
            this.getCatalogs()
        },
        getTags() {
            this.getData('/api/tags/', {category: this.category})
                .then(data => this.topTags = data.map(tag => ({
                    ...tag,
                    selected: false
                })))
                .catch(() => {
                    this.topTags = []
                    console.warn('Ошибка получения тегов')
                })
        },
        getCatalogs(page) {
            if (typeof page === "undefined") {
                page = 1
            }
            const PAGE_LIMIT = 20
            const tags = this.topTags.filter(tag => !!tag.selected).map(
                tag => tag.name
            )

            if (this.selectedSort.selected === 'dec') {
                this.sortType = '-'
            } else {
                this.sortType = ''
            }

            const min = document.querySelector("input[name='minPrice']").value
            const max = document.querySelector("input[name='maxPrice']").value

            if (min !== 0) {
                this.filter.minPrice = min
            }
            if (max !== 5000) {
                this.filter.maxPrice = max
            }
            this.getData("/api/catalog/", {
                page,
                category: this.category,
                sort: this.selectedSort ? this.sortType + this.selectedSort.id : null,
                ...this.filter,
                tags,  // TODO ?tag=foo&tag=bar
                limit: PAGE_LIMIT
            })
                .then(data => {
                    this.catalogCards = data.items
                    this.currentPage = data.currentPage
                    this.lastPage = data.lastPage

                }).catch(() => {
                console.warn('Ошибка при получении каталога')
            })
        }
    },
    mounted() {
        this.selectedSort = this.sortRules?.[1]
            ? {...this.sortRules?.[1], selected: ''}
            : null

        this.getCatalogs()
        this.getTags()
        this.category = location.pathname.startsWith('/catalog/')
            ? Number(location.pathname.replace('/catalog/', ''))
            : null
    },
    data() {
        return {
            pages: 1,
            category: null,
            catalogCards: [],
            currentPage: null,
            lastPage: 1,
            selectedSort: null,
            filter: {
                title: '',
                minPrice: 0,
                maxPrice: 5000,
                freeDelivery: false,
                available: true
            },
            sortType: ''
        }
    }
}