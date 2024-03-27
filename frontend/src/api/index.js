class Api {
    constructor(url, header) {
        this._url = url
        this._header = header
    }

    checkResponse(res) {
        return new Promise((resolve, reject) => {
            if (res.status === 204) {
                return resolve(res)
            }
            const func = res.status < 400 ? resolve : reject
            res.json().then(data => func(data))
        })
    }

    async signin({ username, password }) {
        return await fetch(
            `/api/v1/signin/`,
            {
                method: 'POST',
                headers: this._header,
                body: JSON.stringify({
                    username, password
                })
            }
        ).then(this.checkResponse)
    }

    signout() {

    }

    signup({ first_name, last_name, username, email, hashed_password }) {
        return fetch(
            `/api/v1/signup/`,
            {
                method: 'POST',
                header: this._header,
                body: JSON.stringify({
                    first_name, last_name, username, email, hashed_password
                })
            }
        ).then(this.checkResponse)
    }

    createService({ name, description, price }) {

    }

    getCurentUser() {
        const token = localStorage.getItem('token')
        return fetch(
            `/api/v1/users/me`,
            {
                method: 'GET',
                headers: {
                    ...this._header,
                    'authorization': `Bearer ${token}`
                }
            }
        ).then(this.checkResponse)
    }

    // Service

    getServiceById() {

    }

    getServiceList() {

    }

    deleteService() {

    }


    updateService() {

    }

    // relation User Service
    userService() {

    }
}


export default new Api(process.env.API_URL || 'http://localhost', { 'content-type': 'apllication/json' })