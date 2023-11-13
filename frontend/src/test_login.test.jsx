import { render, screen } from '@testing-library/react';
import Login from './pages/login_page';
import { MemoryRouter } from 'react-router-dom';

describe('Login', () => {
    it('renders the login page yay', () => {
        render(<MemoryRouter>
            <Login />
          </MemoryRouter>);
        expect(screen.getByText('Superset Username:')).toBeInTheDocument();
        expect(screen.getByText('Superset Password:')).toBeInTheDocument();
        expect(screen.getByText('For every child')).toBeInTheDocument();
    });
});