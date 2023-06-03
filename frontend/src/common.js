
import { styled } from '@mui/system';

export const Header = styled('header')({
    position: 'absolute',
    top: '0',
    left: '0',
    right: '0',
    display: 'flex',
    justifyContent: 'flex-start',
    alignItems: 'center',
    width: '100%',
    backgroundColor: '#e8f0fe',
    padding: '0.1rem',
    borderTop: '1px solid #7d68a1',
  });
  
export  const LogoImage = styled('img')({
    width: '50px',
    height: '50px',
    borderRadius: '50%',
  });

export const LogoutButton = styled('button')({
    marginLeft: 'auto',
    marginRight: '1rem',
    padding: '0.5rem 1rem',
    backgroundColor: '#fff',
    color: '#7d68a1',
    border: '1px solid #7d68a1',
    borderRadius: '5px',
    cursor: 'pointer',
    fontWeight: 'bold',
  });

  