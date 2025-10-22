resource "azurerm_kubernetes_cluster" "nexus_cluster" {
  name                = "eternal-nexus"
  location            = azurerm_resource_group.gracealone.location
  resource_group_name = azurerm_resource_group.gracealone.name
  dns_prefix          = "eternalnexus"
  default_node_pool {
    name       = "nexus"
    node_count = 10
    vm_size    = "Standard_B8ms"
  }
  identity {
    type = "SystemAssigned"
  }
}
