### Summary of Changes
The pull request refactors the frontend navigation component to use the new React Router v6 hooks. It removes deprecated `useHistory` calls, replacing them with `useNavigate`, and standardizes the routing configuration across the application.

### Identified Risks
- Some nested routes in the admin dashboard do not have fallback error boundaries, which might result in a blank page if a routing error occurs.
- The lazy loading mechanism for the `Analytics` view was removed, which could negatively impact the initial bundle size and load time.

### Improvement Suggestions
- Reintroduce React.lazy and Suspense for the `Analytics` view to maintain optimal performance.
- Add `<Route errorElement={<ErrorBoundary />}>` to the admin routes to prevent unhandled routing exceptions.
- Add a quick test to ensure the redirects from legacy URLs still point to the correct new locations.

### Confidence Score
Medium
