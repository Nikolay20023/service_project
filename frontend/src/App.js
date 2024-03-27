import './App.css';
import { Switch, Route, useHistory, Redirect, useLocation } from 'react-router-dom'
import React, { useState, useEffect } from 'react';
import { Header, Footer, ProtectedRoute } from './components'
import api from './api'
import cn from 'classnames'
import styles from './styles.module.css'



import {
  Main,
  Cart,
  SignIn,
  Subscriptions,
  Favorites,
  SingleCard,
  SignUp,
  RecipeEdit,
  RecipeCreate,
  User,
  ChangePassword
} from './pages'

import { AuthContext, UserContext } from './contexts';


function App() {
  const [loggedIn, setLoggedIn] = useState(null)
  const [user, setUser] = useState({})
  const [loading, setLoading] = useState(false)
  const [orders, setOrders] = useState(0)
  const [menuToggled, setMenuToggled] = useState(false)
  const location = useState()

  const registration = ({
    first_name,
    last_name,
    username,
    email,
    hashed_password
  })
  api.signup({ first_name, last_name, username, email, hashed_password })
    .then(res => {
      history.push('/signin')
    })
    .catch(err => {
      const error = Object.values(err)
      if (error) {
        alert(error.join(', '))
      }
      setLoggedIn(false)
    })


  const authoriztion = ({
    username, password
  }) => {
    api.signin(
      { username, password }
    ).then(res => {
      if (res.auth_token) {
        localStorage.setItem('token', res.auth_token)
        api.getCurentUser()
          .then(res => {
            setUser(res)
            setLoggedIn(true)

          })
          .catch(err => {
            setLoggedIn(false)
            history.push('/signin')
          })
      } else {
        setLoggedIn(false)
      }
    })
      .catch(err => {
        const error = Object.values(err)
        if (error) {
          alert(error.join(', '))
        }
        setLoggedIn(false)
      })
  }

  const history = useHistory()

  return <AuthContext.Provider value={loggedIn}>
    <UserContext.Provider value={user}>
      <div className={cn("App", {
        [styles.appMenuToggled]: menuToggled
      })}>
        <div
          className={styles.menuButton}
          onClick={_ => setMenuToggled(!menuToggled)}
        >

        </div>
        <Header orders={orders} loggedIn={loggedIn}>
          <ProtectedRoute />
        </Header>
      </div>
    </UserContext.Provider>
  </AuthContext.Provider >

}
