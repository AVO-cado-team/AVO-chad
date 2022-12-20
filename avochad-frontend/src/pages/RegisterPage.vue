<!-- LOGIN PAGE -->
<template>
  <!-- card in center -->
  <q-page-container class="flex flex-center">
    <!-- Notify  -->
    <q-notification
      v-model="notify"
      position="top"
      color="negative"
      message="Invalid email or password"
    />

    <q-card class="q-pa-md">
      <q-card-section>
        <div class="text-h5">Login</div>
      </q-card-section>

      <!-- form -->
      <q-form @submit="onSubmit" @reset="onReset" class="q-pa-md">
        <q-input
          v-model="email"
          label="Email"
          type="email"
          filled
          lazy-rules
          :rules="[val => val.length > 0 || 'Please type something']"
        />
        <q-input
          v-model="password"
          label="Password"
          type="password"
          filled
          lazy-rules
          :rules="[val => val.length > 0 || 'Please type something']"
        />
        <div class="row justify-end">
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
          <q-btn label="Submit" type="submit" color="primary" />
        </div>
      </q-form>
    </q-card>
  </q-page-container>

</template>

<script lang="ts">
import Validator from "../utils/Validator";
import { defineComponent } from "vue";

export default defineComponent({
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
      notify: false
    };
  },
  methods: {
    onSubmit() {
      if (Validator.validateLogin(this.email, this.password)) {
        this.$router.push("/home");
      } else {
        this.notify = true;
      }
    },
    onReset() {
      this.email = "";
      this.password = "";
    }
  }
});

</script>
