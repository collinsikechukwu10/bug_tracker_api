Vue.component("vue-editable", {
  props: {
    value: {
      type: String,
      default: "",
    },
    display: {
      type: String,
      // default: "inline-block",
    },
  },
  computed: {
    listeners() {
      return { ...this.$listeners, input: this.onInput }
    },
  },
  methods: {
    onInput(e) {
      this.$emit("input", e.target.innerText)
    },
  },
  /*html*/
  template: `<p ref="editable" :style="{display: display, textAlign: 'start'}" contenteditable v-on="listeners"></p>`,
  mounted() {
    this.$refs.editable.innerText = this.value
    this.$refs.editable.focus()
  },
})
