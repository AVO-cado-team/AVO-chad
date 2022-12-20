import { Reg } from './models/reg';


interface Session {
  jwt: string;
  timeout: number;
}

let baseUrl = 'http://localhost:9090';

export class Client {
  private session: Session | null = null;

  constructor() {
    let session = localStorage.getItem('session');
    if (session) {
      this.session = JSON.parse(session);
    }
  }

  public register(reg: Reg): Promise<string> {
    return fetch(baseUrl + '/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(reg)
    }).then(
      (response) => {
        if (response.status === 200) {
          // decode the JWT and store it in localStorage
          response.text().then((text) => {
            let payload = JSON.parse(atob(text.split('.')[1]));
            let timeout = payload.exp - payload.iat;
            this.session = { jwt: text, timeout: timeout };
            localStorage.setItem('session', JSON.stringify({ jwt: response.text(), timeout: timeout}));
          });
          return '';
        } else {
          return response.text();
        }
      }
    )
  }


}
