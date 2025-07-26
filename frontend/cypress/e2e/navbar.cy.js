/// <reference types="cypress" />

describe('NavBar Test', () => {
  beforeEach(() => {
    // Intercept unrelated dashboard request
    cy.intercept(
      'GET',
      'http://127.0.0.1:5000/api/v1/dashboard/notifications',
      { statusCode: 200, body: {'status': 'success', 'message': 'Notifications retrieved successfully', 'data': {}} }
    ).as('notificationsRequest')
    cy.visitPage('/dashboard')
    cy.wait('@notificationsRequest')
  })

  // ASSETS
  it('There is an icon for every nav-item (Inicio, etc.)', () => {
    // For evey nav-item
    cy.get('.nav-item .icon').each(($el) => {
      cy.wrap($el).should('exist')
      // Check that the src is not empty
      cy.wrap($el).invoke('attr', 'src').should('not.be.empty')
    })
  })

  it('There is an icon for every nav-option (Log-out, etc.)', () => {
    // For evey nav-option
    cy.get('.nav-option .option').each(($el) => {
      cy.wrap($el).should('exist')
      // Check that the src is not empty
      cy.wrap($el).invoke('attr', 'src').should('not.be.empty')
    })
  })

  it('Items change colour when hovered', () => {
    // For evey nav-item
    cy.get('.nav-item .icon').each(($el) => {
      cy.wrap($el)
        .invoke('attr', 'src')
        .then((initialSrc) => {
          // Trigger mouseover
          cy.wrap($el).trigger('mouseover')

          // Assert new src is different
          cy.wrap($el)
            .invoke('attr', 'src')
            .should('not.eq', initialSrc)

          // Trigger mouseleave
          cy.wrap($el).trigger('mouseleave')

          // Assert it's back to original
          cy.wrap($el)
            .invoke('attr', 'src')
            .should('eq', initialSrc)
        })
    })
  })

  it('Options change colour when hovered', () => {
    // For evey nav-option
    cy.get('.nav-option .option').each(($el) => {
      cy.wrap($el)
        .invoke('attr', 'src')
        .then((initialSrc) => {
          // Trigger mouseover
          cy.wrap($el).trigger('mouseover')

          // Assert new src is different
          cy.wrap($el)
            .invoke('attr', 'src')
            .should('not.eq', initialSrc)

          // Trigger mouseleave
          cy.wrap($el).trigger('mouseleave')

          // Assert it's back to original
          cy.wrap($el)
            .invoke('attr', 'src')
            .should('eq', initialSrc)
        })
    })
  })

  it('Items redirect to the right pages', () => {
    const expectedRoutes = [
      '/dashboard',
      '/students',
      '/tutors',
      '/companies',
      '/assignments'
    ]
    const expectedIntercepts = [
      'http://127.0.0.1:5000/api/v1/dashboard/notifications',
      'http://127.0.0.1:5000/api/v1/students',
      'http://127.0.0.1:5000/api/v1/tutors',
      'http://127.0.0.1:5000/api/v1/companies',
      'http://127.0.0.1:5000/api/v1/assignments'
    ]

    cy.get('.nav-item').then(($items) => {
      // Cypress .each() queues all actions at once which causes DOM problems
      function testNavItem (index) {
        if (index >= $items.length) return

        cy.intercept(
          'GET',
          expectedIntercepts[index],
          { statusCode: 200, body: {'status': 'success', 'message': 'Data retrieved successfully', 'data': {}} }
        ).as('redirectRequest')
        cy.get('.nav-item').eq(index).click()
        cy.wait('@redirectRequest')
        cy.location('pathname').should('eq', expectedRoutes[index])

        cy.getFullUrl('/dashboard').then((fullUrl) => {
          // Intercept unrelated dashboard request
          cy.intercept(
            'GET',
            'http://127.0.0.1:5000/api/v1/dashboard/notifications',
            { statusCode: 200, body: {'status': 'success', 'message': 'Notifications retrieved successfully', 'data': {}} }
          ).as('dashboardRequest')
          cy.visit(fullUrl).then(() => {
            testNavItem(index + 1)
          })
          cy.wait('@dashboardRequest')
        })
      }
      testNavItem(1)
    })
  })

  it('Log out works', () => {
    // Intercept logout request
    cy.intercept(
      'POST',
      'http://127.0.0.1:5000/api/v1/landing/logout',
      { statusCode: 200, body: {'status': 'success'} }
    ).as('logoutRequest')
    cy.get('.nav-option').last().click()
    cy.wait('@logoutRequest')
    cy.url().should('include', '/landing')
  })
})
