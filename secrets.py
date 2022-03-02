from toml import dumps, load, loads
import streamlit as st
credentials = {
  "type": "service_account",
  "project_id": "petrochamp",
  "private_key_id": "1a3b121928c385590a0d98f642826896f2a87a2f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC31UAWe9oqOi4i\n+lJfzqfEu3/SEp0X1/zyW3e9xjbkwklLei8ct1gWCoSCsew/bkvoatf7/bG69HH7\nC9x/IIGBMT+bx3eBupnEco+mh1mi/15VCwi9XvPvPlF5nm8SpfRPyzSWbe44g+cl\nVFL/eYQLDpp3PN2v5oB0aK8kS89/oTSPyT/Tw/UseQjy1XaSOWpq0YTjEutZSW79\nA4eHJ0kSS2Rv7WFN8bOZICSIasCWbJqfive+e/kr8+zZAZr2hr+dXwBRex+0xvF5\nvJ5LarCytdLUh1Iey2F2ELDsep50jLRnOw8GeyiqUuWTDdf5N2HxuYIkdljEL8oy\nmtdh5uoTAgMBAAECggEAAQFvINBboKiB0RoqcjC4tThLWjRU3KkHTrIWZRjc+wJf\nEUUhVdhg6Hn1QJvFjZFGZAaVmODJ5JpqtzNY6O8eFj1VOj5slm6VYcA4rfIGmQAp\nnXB6g0KuNexS2MX3mJQE0pzrdDk0uOVr0cX00EXzZXYWfTl9gvVRVZGvB5VMlMek\nGHURX80ewQdNO8MLQTlIYgtnqGA7pYRRexKhtuiAbYFSmhdYi0OyZ/v1g7oYbsvb\nsDkUDkYtsRF3ujiHLEHMsXTNd0Eo3eYLPD2Yot64vM7HnAsyjRSj9H16idp0ENJJ\nN40EE37XKtXVs5AbUjNmxxWD93vq9CZ7L7UFE7R9/QKBgQDhIpC+kHaxV1/H3vNf\nMUUqK9tqomFIG+XcvFjqOAZwvXaz7Udt7JuhinxCKfU//1WR24npZdxjPJlLciAG\newQP3gd7AqxhL0L/37wnhJM6fHhIo1BmkwXHth92APBXfMAI+kazVlkXMuQU7ntk\n5MCF9Zxs4Tt8enHnlRxD1y5NhQKBgQDRCSHGRAUaTyrrV4X2Vu4a4TXebQuYtQYH\nFWJJYBytezZxYA1ljibRqPqlifCRctIixZlQgSi29rz2mcGFo+BEc6bXB6qYoiSE\ngA7VatN1HqnIcZ7AgJEW+otzz1brucekwh8c1xw9Qd/4tGtB8gd6KlHjokkvyZwV\nLk6HmU+AtwKBgQDLcQbHjZgUTVZ6MNhPzyAnKZaPV8j89mjS/UiD7rizLCKWGPcR\nOFyyr4f16iB7Amr68R5A0RFEg8Aq0yhpcsSK6iJsYFARSjoLKszGESFSGqQ/T4Ua\nDAWPIN5xLgwBovONqUw2RvMe6Zf96juLQsNOylHeefHdXHCNysrN6ycmWQKBgQCO\npqC54OlqjuRHPq9Y8PIEvfQ5GklzqPW4F8u/Lyvi59a7gEUkLOIo6hxCo+PcHnNw\n71A1NC9IzREfaMY8IR2HGTWeQMkW6G/rTEjTM9eicY6ED6W60QIyoEBShAhZTasE\nsMTytYm79ByYaOdZVYXsxLylj7ZKOledzMAioWkz+QKBgHyYoFl9FM9WR1evq9Tn\nvc0hdUhTCPxGgeFaXPHac2sKk0MBSfUcwwJ/1x8ECxwymNZBOp97Cq88UNJ6zKlB\nJGTxjQjHtctr1Ns7Q7UUw+PxYNU0Y5CvC//QQigPrDZXfoJfyOhYcjgWKtNGsbk4\niqqlq/t/UCjrKdZn0V2brPPN\n-----END PRIVATE KEY-----\n",
  "client_email": "service-account@petrochamp.iam.gserviceaccount.com",
  "client_id": "110869707163213607990",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40petrochamp.iam.gserviceaccount.com"
}

toml = dumps(credentials)

st.text_area(label="Toml:", value=toml)

dic = loads(toml)
st.text(dic)