resource "azurerm_kubernetes_cluster" "sentient" {
  name                = "sentient-cloud"
  location            = azurerm_resource_group.gracealone.location
  resource_group_name = azurerm_resource_group.gracealone.name
  dns_prefix          = "sentient"
  default_node_pool {
    name       = "agentpool"
    node_count = 3
    vm_size    = "Standard_B2s"
  }
  identity {
    type = "SystemAssigned"
  }
}
