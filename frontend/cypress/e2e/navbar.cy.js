/// <reference types="cypress" />
const dashboardUrl = 'http://localhost:5000/dashboard'

describe('NavBar Test', () => {
  beforeEach(() => {
    cy.visit(dashboardUrl)
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

    cy.get('.nav-item').then(($items) => {
      // Cypress .each() queues all actions at once which causes DOM problems
      function testNavItem (index) {
        if (index >= $items.length) return

        cy.get('.nav-item').eq(index).click()
        cy.location('pathname').should('eq', expectedRoutes[index])

        cy.visit(dashboardUrl).then(() => {
          testNavItem(index + 1)
        })
      }
      testNavItem(0)
    })
  })

  it('Log out works', () => {
    cy.get('.nav-option').last().click()
    cy.url().should('include', '/landing')
  })
})
