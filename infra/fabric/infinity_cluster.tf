resource "azurerm_kubernetes_cluster" "infinity_cluster" {
  name                = "infinite-intelligence"
  location            = azurerm_resource_group.gracealone.location
  resource_group_name = azurerm_resource_group.gracealone.name
  dns_prefix          = "infinitecore"
  default_node_pool {
    name       = "infinity"
    node_count = 8
    vm_size    = "Standard_B4ms"
  }
  identity {
    type = "SystemAssigned"
  }
}
