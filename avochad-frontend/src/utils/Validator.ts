export default class Validator {
  static passwordValidation (password: string): boolean {
    return /^[A-Za-z\d]{8,}$/.test(password)
  }

  static emailValidation (email: string) : boolean {
    return /^(?=.{1,254}$)(?=.{1,64}@)[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*@[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$/.test(email)
  }

  static validateLogin (email: string, password: string): boolean {
    return this.emailValidation(email) && this.passwordValidation(password)
  }
}
